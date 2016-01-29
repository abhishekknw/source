angular.module('machadaloCommon')
.directive('imageDisplay', function() {
  return {
    restrict: 'E',
    templateUrl: 'modules/common/imagedisplay/image-display.tmpl.html',
    link: function(scope, element, attr) {
      //scope.societyAddress1 = "Park Street";
      scope.societyAddress2 = "Powai";
      scope.societyCity = "Mumbai";
      scope.localityRating = "4";
      scope.machadaloIndex = "4";
      scope.societyRating = "5";
      scope.totalAdspaces = "19";
      scope.societyAddress1 = attr.societyAddress1;
      console.log(scope.societyAddress1);
    }};
  });
