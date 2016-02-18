angular.module('machadaloCommon')
.directive('imageDisplay', function() {
  return {
    restrict: 'E',
    //scope: {images:"="},
    templateUrl: 'modules/common/imagedisplay/image-display.tmpl.html',
    link: function(scope, element, attr) {
      //scope.societyAddress1 = "Park Street";
      //scope.societyAddress2 = "Powai";
      //scope.societyCity = "Mumbai";
      //scope.localityRating = attr.society_locality;
      //scope.machadaloIndex = "4";
      //scope.societyRating = "5";
      //scope.totalAdspaces = "19";
      //scope.societyAddress1 = attr.societyAddress1;
      scope.mainconfig = {
        dots:false,
        autoplay:true,
        autoplaySpeed:2000, infinite:true, slidesToShow:1, slidesToScroll:1,
        asNavFor:"thumb-slider",
        method: {}
      }
      scope.thumbconfig = {
        dots:false,
        autoplay:false, slidesToShow:5, slidesToScroll:1,
        asNavFor:"main-slider",
        method:{}
      }
    }};
  });
