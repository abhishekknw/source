angular.module('machadaloCommon')
.factory('machadaloHttp', ['$http', '$rootScope', function($http, $rootScope) {
   var machadaloHttp = {};
   machadaloHttp.baseURL = APIBaseUrl;

   var extendHeaders = function(config) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = 'JWT ' + $rootScope.globals.currentUser.token;
   }

   angular.forEach(['get', 'delete', 'head', 'jsonp'], function (name) {
      machadaloHttp[name] = function(url, config) {
         config = config || {};
         extendHeaders(config);
         return $http[name](machadaloHttp.baseURL + url, config);
      };
   });

   angular.forEach(['post', 'put'], function (name) {
      machadaloHttp[name] = function(url, data, config) {
         config = config || {};
         extendHeaders(config);
         return $http[name](machadaloHttp.baseURL + url, data, config);
      };
   });

   return machadaloHttp;
}])
