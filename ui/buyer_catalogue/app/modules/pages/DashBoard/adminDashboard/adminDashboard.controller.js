"use strict";
angular.module('catalogueApp')
    .controller('adminDashboardController', function($scope, $rootScope, $stateParams, $window, $location, currentProposalService ,$http, constants, permissions, commonDataShare, $mdSidenav, adminDashboardService) {

      $scope.viewContent = 'todayStatus';
      $scope.views = {
        chart : true,
        table : false,
      }
      $scope.queries = {
        bookingStatus : 'booking_status',
        supplierCode : 'supplier_code',
        phase  : 'phase',
      }
      $scope.getView = function(view){
        console.log(view);
        for( var key in $scope.views ) {
          $scope.views[key] = false;
        }
        $scope.views[view] = true;

        console.log($scope.views);
      }
      $scope.campaignStatus = {
        ongoing_campaigns : {
            header : 'Ongoing Campaign', value : 'ongoing_campaigns',
          },
        upcoming_campaigns : {
          header : 'Upcoming Campaign', value : 'upcoming_campaigns',
        },
        completed_campaigns : {
          header : 'Completed Campaign', value : 'completed_campaigns',
        },
        all_campaigns : {
          header : 'All Campaigns', value : 'all_campaigns',
        }
      }
    $scope.getCampaignsByStatus = function(campaign){
      $scope.activity = $scope.campaignStatus[campaign].header;
      if(campaign == $scope.campaignStatus.all_campaigns.value){
        $scope.campaignList = $scope.campaignData.ongoing_campaigns.concat($scope.campaignData.upcoming_campaigns,$scope.campaignData.completed_campaigns);
      }else{
        console.log(campaign);
        $scope.campaignList = $scope.campaignData[campaign];
      }

      // $scope.getView('table');
    }

    $scope.colours = ['#ff0000', '#D78D43', '#00ff00'];
    $scope.labels = ["Ongoing Campaigns", "Upcoming Campaigns", "Completed Campaigns"];
    console.log($rootScope);
    $scope.queryDate = {};
    $scope.options = { legend: { display: true, position: 'bottom' } };

    var category = $rootScope.globals.userInfo.profile.organisation.category;
    var orgId = $rootScope.globals.userInfo.profile.organisation.organisation_id;
    $scope.getCampaigns = function(date){
      if(!date)
        date = new Date();
      date = commonDataShare.formatDate(date);
      date = date + ' 00:00:00';

      console.log(date);
      adminDashboardService.getCampaigns(orgId, category, date)
      .then(function onSuccess(response){
        console.log(response);
        $scope.campaignData = response.data.data;
        $scope.campaigns = [$scope.campaignData.ongoing_campaigns.length,$scope.campaignData.upcoming_campaigns.length,$scope.campaignData.completed_campaigns.length];
        $scope.getCampaignsByStatus($scope.campaignStatus.all_campaigns.value);
        console.log($scope.campaignLength);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.getCampaigns();

    $scope.getCampaignDetails = function(campaignId,query){
      $scope.campaignId = campaignId;
      adminDashboardService.getCampaignDetails(campaignId,query)
      .then(function onSuccess(response){
        console.log(response);
        $scope.chartData = [];
        $scope.chartLebels = [];

        setChartData(response.data.data,query);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    $scope.chartData = [];
    $scope.chartLebels = [];
    var getBookingStatus = function(item){
      if(item.booking_status)
          return constants[item.booking_status];
      return constants.NBK;
    }
    var getPhase = function(item){
      if(item.phase)
          return item.phase;
      return constants.no_phase;
    }
    var getLabelName = function(item,query){
      if($scope.queries.bookingStatus == query){
        return constants[item.supplier_code] + " : " + getBookingStatus(item) +" ,Count: " + item.total;
      }
      if($scope.queries.supplierCode == query){
        return constants[item.supplier_code] + " Count: " + item.total;
      }
      if($scope.queries.phase == query){
        return constants[item.supplier_code] + " : "  + ",Phase :"+ getPhase(item) + ", " + getBookingStatus(item) + " ,Count: " + item.total;
      }
    }
    var setChartData = function(data,query){
      angular.forEach(data, function(item){
        $scope.chartData.push(item.total);
        var labelName = getLabelName(item,query);
        $scope.chartLebels.push(labelName);
      })
    }
    var getAllCampaignsData = function(){
      adminDashboardService.getAllCampaignsData(orgId, category)
      .then(function onSuccess(response){
        console.log(response);
        $scope.allCampaignsData = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
    }

    $scope.changeView = function(view){
      $scope.viewContent = view;
      console.log($scope.viewContent);
    }
    getAllCampaignsData();

    $scope.getAssignedIdsAndImages = function(date,type,inventory){
      adminDashboardService.getAssignedIdsAndImages(orgId, category, type, date, inventory)
      .then(function onSuccess(response){
        console.log(response);
        $scope.allCampaignsData1 = response.data.data;
      }).catch(function onError(response){
        console.log(response);
      })
    }
})
