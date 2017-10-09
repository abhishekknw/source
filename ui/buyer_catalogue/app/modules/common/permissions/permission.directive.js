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
                  if(elem[0].tagName == 'BUTTON' || elem[0].tagName == 'INPUT')
                    attrs.$set('disabled', 'disabled');
                  else
                    elem.hide();
                }
            });
       }
   }
}]);
