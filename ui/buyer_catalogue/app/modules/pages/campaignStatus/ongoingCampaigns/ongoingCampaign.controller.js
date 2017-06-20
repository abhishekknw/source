"use strict";
angular.module('catalogueApp')
    .controller('OngoingCampaignCtrl', function($scope, $rootScope, $stateParams, $window, $location, ongoingCampaignService ,$http, constants) {
      $scope.headers = [
        {header : 'Campaign Name'},
        {header : 'Created At'},
        {header : 'Created By'},
        {header : 'Created For'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Percent Completed'},
        {header : 'Booked Spaces'},
        {header : 'Completed'},
        {header : 'Remaining'},
        {header : 'Comments'},
        {header : 'Total Impressions'},
        {header : 'Lead Count'},
      ]
    });
