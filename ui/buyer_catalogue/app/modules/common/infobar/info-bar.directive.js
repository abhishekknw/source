angular.module('machadaloCommon')
.directive('infoBar', function() {
  return {
  restrict: 'AEC',
  templateUrl: 'modules/common/infobar/info-bar.tmpl.html',
  controller: ['$rootScope', function($rootScope, element, attrs) {
    //scope.campaignname = attrs.campaignname;
    //$scope.businessname = attrs.businessname;
    //$scope.societyname = attrs.societyname;
  }]};
});
