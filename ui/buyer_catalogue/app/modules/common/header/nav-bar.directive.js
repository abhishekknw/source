angular.module('machadaloCommon')
.directive('navBar', function($window,$rootScope,constants,$timeout) {
  return {
    templateUrl: 'modules/common/header/nav-bar.tmpl.html',
    link: function($scope, element, attrs) {
              $scope.user_code = $window.localStorage.user_code;


                  $timeout(function () {
                    angular.forEach($rootScope.globals.userInfo.groups, function(group){
                      console.log(constants);
                      if(group.name == constants.campaign_manager){
                        $scope.campaignAccessAllowed = false;                                                
                      }
                      })

                  })
                  if($rootScope.globals.userInfo.is_superuser == true){
                      $scope.campaignAccessAllowed = true;
                    }
                if($rootScope.globals.userInfo.is_superuser == true){
                    $scope.showData = true;
                  }
                // Do some stuff
              $scope.closeModal = function(){
                $('#menuModal').modal('hide');
                 $('body').removeClass('modal-open');
                 $('.modal-backdrop').remove();
              }
        }
  };
});
