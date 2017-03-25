angular.module('machadaloCommon')
.directive('navBar', function($window) {
  return {
    templateUrl: 'modules/common/header/nav-bar.tmpl.html',
    link: function($scope, element, attrs) {
              $scope.user_code = $window.localStorage.user_code;
              if($scope.user_code == 'root')
                $scope.showData =true;
              if($scope.user_code == 'guestUser')
                $scope.isGuestUser = true;
              if($scope.user_code == 'agency')
                $scope.isAgency = true;
                // Do some stuff
              $scope.closeModal = function(){
                $('#menuModal').modal('hide');
                 $('body').removeClass('modal-open');
                 $('.modal-backdrop').remove();
              }
        }
  };
});
