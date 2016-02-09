angular.module('machadaloCommon')
.directive('filterTab', function() {
  return {
  restrict: 'E',
  templateUrl: 'modules/common/filters/filter-tab.tmpl.html',
  link: function(scope, element, attrs) {
    scope.demo2 = {
        range: {
            min: 100,
            max: 10050
        },
        minPrice: 1000,
        maxPrice: 4000
    };
  }};
});
