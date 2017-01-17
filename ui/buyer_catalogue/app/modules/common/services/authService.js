'use strict';

angular.module('Authentication')

.factory('AuthService',
    ['$http', '$location', '$rootScope', '$window', '$timeout',
    function ($http, $location, $rootScope, $window, $timeout) {

        var authService = {};
        var storageCredentials = 'machadalo-credentials';
        var storagePermissions = 'machadalo-permissions';
        var apiHost = APIBaseUrl;
        var permissions = {};

        authService.Login = function (username, password, callback) {
            $http.post(apiHost + 'api-token-auth/', { username: username, password: password })
                .success(function (response) {
                  $window.localStorage.user_code = response.user_code;
                   if (response.token) {
                      authService.SetCredentials(response);
                      response.logged_in = true;
                      callback(response);
                   }
                   else {
                      response.logged_in = false;
                      callback(response);
                   }
                })
                .error(function (response) {
                  if (!response)
                    response = {};
                    response.logged_in = false;
                    response.message = "Invalid username or password";
                   callback(response);
                });
           };

        authService.logoutEvent = function (e) {
           var logging_out = true;
           if (e) {
              logging_out = false;
              if (e.originalEvent) e = e.originalEvent;
              if (e.key == storageCredentials) {
                 if (e.newValue == null || e.newValue.length == 0) {
                    logging_out = true;
                 }
              }
           }
           return logging_out;
        }

        authService.Logout = function () {
          $window.localStorage.clear();
          $rootScope.user='';
            $rootScope.role=0;
           authService.ClearCredentials();
           if ($location.path() != "/login") $rootScope.globals.requestedPath = $location.path();
           $location.path('/login');
        }

        authService.isAuthenticated = function () {
           authService.GetCredentials();
           if ($rootScope.globals && $rootScope.globals.currentUser && $rootScope.globals.currentUser.token) {
              return true;
           }
           return false;
        }

        authService.Clear = function() {
           authService.ClearCredentials();
        }

        authService.UserInfo = function() {
           return authService.GetCredentials();
        }


        authService.SetCredentials = function (response) {
            $rootScope.globals = $rootScope.globals || {};
            $rootScope.globals.currentUser = $rootScope.globals.currentUser || {};
            for (var property in response) {
               if (response.hasOwnProperty(property)) {
                  $rootScope.globals.currentUser[property] = response[property];
               }
            }
            if ($window.localStorage) {
               var json = JSON.stringify($rootScope.globals.currentUser);
               if (json) {
                  $window.localStorage.removeItem(storageCredentials);
                  $window.localStorage.setItem(storageCredentials, json);
               }
               else {
                  $rootScope.globals.currentUser = {};
               }
            }
        };

        authService.GetCredentials = function () {
           if ($window.localStorage) {
              var json = $window.localStorage.getItem(storageCredentials);
              if (json) {
                 try {
                    $rootScope.globals.currentUser = JSON.parse(json);
                    return $rootScope.globals.currentUser;
                 }
                 catch (e) {
                    authService.ClearCredentials();
                 }
              }
           }
           $rootScope.globals.currentUser = {};
           return null;
        };

        authService.ClearCredentials = function () {
            if ($rootScope.globals){
              $rootScope.globals.currentUser = {};
            }
            if ($window.localStorage) {
               $window.localStorage.removeItem(storageCredentials);
            }
        };

        return authService;
    }])
