angular.module('machadaloPages')
.controller('guestHomePageController',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService','errorHandler',
    function ($scope, $rootScope, $window, $location, pagesService, errorHandler) {
      var $jq = jQuery.noConflict();
      var $jp = jQuery.noConflict();
      $jq(document).ready(function(){
        $('.campaignCarousel').slick({
         slidesToShow: 4,
         slidesToScroll: 1,
         autoplay: true,
         autoplaySpeed: 1000,
        });
      });
      $jp(document).ready(function(){
        $('.spaceCarousel').slick({
          // prevArrow : ' <img src="img/cleft.png"></img>',
          // nextArrow : '<img src="img/cright.png"></img>',
           slidesToShow: 3,
           slidesToScroll: 1,
           autoplay: true,
           autoplaySpeed: 1000,
        });
      });
    }]);
