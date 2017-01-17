angular.module('machadaloCommon')
.directive('navBar', function($window) {
  return {
    templateUrl: 'modules/common/header/nav-bar.tmpl.html',
    link: function($scope, element, attrs) {
              $scope.user_code = $window.localStorage.user_code;
              if($scope.user_code == '0')
                $scope.showData =true;
                // Do some stuff
        }
  };
});
