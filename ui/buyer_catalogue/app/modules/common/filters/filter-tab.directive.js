angular.module('machadaloCommon')
.directive('filterTab', function() {
  return {
  restrict: 'E',
  templateUrl: 'modules/common/filters/filter-tab.tmpl.html',
  link: function(scope, element, attrs) {
    scope.slider_translate = {
       minValue: 100,
       maxValue: 400,
       options: {
           ceil: 500,
           floor: 0,
           translate: function (value) {
               return '$' + value;
           }
       }
   };
  }};
});
