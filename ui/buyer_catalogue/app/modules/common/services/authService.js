'use strict';

angular.module('Authentication')

.factory('AuthService',
    ['$http', '$location', '$rootScope', '$window', '$timeout','commonDataShare',
    function ($http, $location, $rootScope, $window, $timeout, commonDataShare) {

        var authService = {};
        var storageCredentials = 'machadalo-credentials';
        var storagePermissions = 'machadalo-permissions';
        var apiHost = APIBaseUrl;
        var permissions = {};
        var user_codes = {
          '0' : 'root',
          '03': 'agency',
          '99': 'guestUser',
        };

        authService.Login = function (username, password, callback) {
            $http.post(apiHost + 'api-token-auth/', { username: username, password: password })
                .then(function onSuccess(response) {
                  $window.localStorage.user_code = user_codes[response.data.user_code];
                   if (response.data.token) {
                      authService.SetCredentials(response.data);
                      response.data.logged_in = true;
                      callback(response.data);
                      commonDataShare.getUserDetails($rootScope.globals.currentUser.user_id)
                      .then(function onSuccess(response){
                        console.log(response);
                        if(response.data.data.is_superuser == true)
                          $window.localStorage.isSuperUser = true;
                        else
                          $window.localStorage.isSuperUser = false;
                      }).catch(function onError(response){
                        console.log(response);
                      });
                   }
                   else {
                      response.data.logged_in = false;
                      callback(response.data);
                   }
                })
                .catch(function onError(response) {
                  if (!response.data)
                    response.data = {};
                    response.logged_in = false;
                    response.message = "Invalid username or password";
                   callback(response.data);
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
