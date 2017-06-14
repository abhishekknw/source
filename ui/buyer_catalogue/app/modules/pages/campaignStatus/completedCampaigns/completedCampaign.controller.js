"use strict";
angular.module('catalogueApp')
    .controller('CompletedCampaignCtrl', function($scope, $rootScope, $stateParams, $window, $location, completedCampaignService ,$http, constants) {
      $scope.headers = [
        {header : 'Campaign Name'},
        {header : 'Created At'},
        {header : 'Created By'},
        {header : 'Created For'},
        {header : 'Total Impression'},
        {header : 'Leads'},
        {header : 'Comments'},
      ]
    });
