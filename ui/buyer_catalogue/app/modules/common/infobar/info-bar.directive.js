angular.module('machadaloCommon')
.directive('infoBar', function() {
  return {
  restrict: 'E',
  templateUrl: 'modules/common/infobar/info-bar.tmpl.html',
  link: function(scope, element, attrs) {
    //scope.campaignname = attrs.campaignname;
    scope.businessname = attrs.businessname;
    scope.societyname = attrs.societyname;
  }};
});
