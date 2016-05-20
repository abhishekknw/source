angular.module('machadaloPages')
.controller('CreateProposalCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService','ngDialog',
    function ($scope, $rootScope, $window, $location, pagesService, ngDialog) {
    $scope.clickToOpen = function () {
        ngDialog.open({ template: 'templateId'});
    };
}]);
