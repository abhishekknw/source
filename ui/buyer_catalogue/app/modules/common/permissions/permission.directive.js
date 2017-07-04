angular.module('Authentication')
.directive('permission', ['AuthService', function(AuthService) {
   return {
       restrict: 'A',
       scope: {
          permission: '='
       },

       link: function (scope, elem, attrs) {
            scope.$watch(AuthService.isLoggedIn, function() {
                if (AuthService.userHasPermission(scope.permission)) {
                    elem.show();
                } else {
                    elem.hide();
                }
            });
       }
   }
}]);
