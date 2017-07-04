"use strict";
angular.module('catalogueApp')
    .controller('UpcomingCampaignCtrl', function($scope, $rootScope, $stateParams, $window, $location, upcomingCampaignService ,$http, constants) {
      $scope.headers = [
        {header : 'Campaign Name'},
        {header : 'Created At'},
        {header : 'Created By'},
        {header : 'Created For'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Total Impressions'},
      ]
    });
