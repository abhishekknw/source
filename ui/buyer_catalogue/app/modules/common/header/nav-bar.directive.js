angular.module('machadaloCommon')
.directive('navBar', function($window,$rootScope,constants,$timeout, permissions) {
  return {
    templateUrl: 'modules/common/header/nav-bar.tmpl.html',
    link: function($scope, element, attrs) {
              $scope.perm = permissions.navBar;
              // Do some stuff
              $scope.closeModal = function(){
                $('#menuModal').modal('hide');
                 $('body').removeClass('modal-open');
                 $('.modal-backdrop').remove();
              }
        }
  };
});
