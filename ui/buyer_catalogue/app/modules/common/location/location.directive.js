var myApp = angular.module('machadaloCommon', []);

myApp.directive('googleplace', ['$rootScope' , function(rootScope) {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, model) {
            var options = {
                types: [],
                componentRestrictions: {country: 'in'}
            };
            scope.gPlace = new google.maps.places.Autocomplete(element[0], options);

            google.maps.event.addListener(scope.gPlace, 'place_changed', function() {
                scope.$apply(function() {
                    model.$setViewValue(element.val());
                     scope.details = scope.gPlace.getPlace();
                     console.log(scope.details);
                      rootScope.$broadcast('place_changed', scope.details);
                });
            });
        }
    };
}]);
// function MyCtrl($scope) {
//     $scope.gPlace;
// }
