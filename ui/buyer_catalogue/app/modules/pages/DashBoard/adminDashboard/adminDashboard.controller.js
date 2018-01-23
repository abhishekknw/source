"use strict";
angular.module('catalogueApp')
    .controller('adminDashboardController', function($scope, $rootScope, $stateParams, $window, $location, currentProposalService ,$http, constants, permissions, commonDataShare, $mdSidenav, adminDashboardService) {

      $scope.viewContent = 'todayStatus';
      $scope.myPercentModel = 40;
      $scope.selectedItem = {};
      var category = $rootScope.globals.userInfo.profile.organisation.category;
      var orgId = $rootScope.globals.userInfo.profile.organisation.organisation_id;
      $scope.orgInfo = $rootScope.globals.userInfo.profile;
      $scope.inventoryActivityCountData = [];
      $scope.invActDateList = [];
      $scope.campaignDataList = [];
      $scope.views = {
        all_campaigns : true,
        chart : false,
        pmatrics : false
      }
      $scope.queryHeaders = [
        {header : 'Supplier Type', value : 'supplier_code'},
        {header : 'Booking Status', value : 'booking_status'},
        {header : 'Completed Campaigns', value  : 'completed_campaigns'},
        {header : 'Ongoing Campaigns', value  : 'ongoing_campaigns'},
        {header : 'Upcoming Campaigns', value  : 'upcoming_campaigns'},
      ];
      $scope.queries = {
        bookingStatus : 'booking_status',
        supplierCode : 'supplier_code',
        phase : 'phase'
      };
      $scope.invKeys = [
        {header : 'POSTER'},
        {header : 'STANDEE'},
        {header : 'STALL'},
        {header : 'FLIER'},
      ];
      $scope.actKeys = [
        {header : 'RELEASE'},
        {header : 'AUDIT'},
        {header : 'CLOSURE'},
      ];
      $scope.supHeaders = [
        {header : 'Campaign Name'},
        {header : 'Supplier Name'},
        {header : 'Inventory Name'},
        {header : 'Activity Name'},
        {header : 'Images'},
      ];
      var campaignDataStruct = {
        id : '',
        supplier_id : '',
        proposal_name : '',
        inv_id : '',
        inv_type : '',
        images : [],
        act_name : '',
        act_date : '',
        reAssign_date : '',
      };
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
        // $scope.campaignList = $scope.campaignData.ongoing_campaigns.concat($scope.campaignData.upcoming_campaigns,$scope.campaignData.completed_campaigns);
      }else{
        console.log(campaign);
        // $scope.campaignList = $scope.campaignData[campaign];
      }
    }

    $scope.colours = ['#ff0000', '#D78D43', '#00ff00'];
    $scope.labels = ["Ongoing Campaigns", "Upcoming Campaigns", "Completed Campaigns"];
    console.log($rootScope);
    $scope.queryDate = {};
    $scope.options = { legend: { display: true, position: 'bottom' } };


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
      if(query != $scope.queries.supplierCode && query != $scope.queries.bookingStatus){
        console.log("hello",$scope.campaignData[query].length );
        $scope.chartData = [];
        $scope.chartLebels = [];
        $scope.chartData.push($scope.campaignData[query].length);
        $scope.chartLebels.push('count : ' + $scope.campaignData[query].length);
      }
      else{
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
        return getBookingStatus(item) +" : " + item.total;
      }
      if($scope.queries.supplierCode == query){
        return constants[item.supplier_code] + " : " + item.total;
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
        $scope.count = 0;
        $scope.invActDateList = [];
        // $scope.inventoryActivityCountData = response.data.data;
        angular.forEach(response.data.data, function(data,key){
            $scope.inventoryActivityCountData[key] = sortObject(data);
            $scope.invActDateList = $scope.invActDateList.concat(Object.keys($scope.inventoryActivityCountData[key]));
        })
        $scope.invActDateList = Array.from(new Set($scope.invActDateList));
        $scope.invActDateList.sort().reverse();
        $scope.getDate($scope.count);
      }).catch(function onError(response){
        console.log(response);
      })
    }

    $scope.changeView = function(view){
      $scope.viewContent = view;
    }
    getAllCampaignsData();

    $scope.getAssignedIdsAndImages = function(date,type,inventory){
      console.log(date,type,inventory);
      adminDashboardService.getAssignedIdsAndImages(orgId, category, type, date, inventory)
      .then(function onSuccess(response){
        console.log(response);
        $scope.campaignData = response.data.data;
        $scope.campaignDataList = [];
        createList();
        console.log($scope.campaignDataList);
      }).catch(function onError(response){
        console.log(response);
      })
    }
    function sortObject(obj) {
      return Object.keys(obj).sort().reverse().reduce(function (result, key) {
          result[key] = obj[key];
          return result;
      }, {});
    }
    $scope.count = 0;
    $scope.getDate = function(count){
      $scope.date =  $scope.invActDateList[count];
    }
    $scope.getPercent = function(num1,num2){
      var percent = num1/num2*100;
      return percent;
    }
    function createList(){
      angular.forEach($scope.campaignData.shortlisted_suppliers,function(suppliers,spaceId){
        angular.forEach($scope.campaignData.shortlisted_inventories,function(inventories,invId){
          if($scope.campaignData.shortlisted_inventories[invId].shortlisted_spaces_id == spaceId){
            angular.forEach($scope.campaignData.inventory_activities,function(activities,actId){
              if($scope.campaignData.inventory_activities[actId].shortlisted_inventory_id == invId){
                angular.forEach($scope.campaignData.inventory_activity_assignment,function(invAssignments,assignId){
                  if($scope.campaignData.inventory_activity_assignment[assignId].inventory_activity_id == actId){
                    var data = angular.copy(campaignDataStruct);
                    data.id = assignId;
                    data.supplier_id = $scope.campaignData.shortlisted_suppliers[spaceId].supplier_id;
                    data.supplier_name = $scope.campaignData.shortlisted_suppliers[spaceId].supplier_detail.name;
                    data.proposal_name = $scope.campaignData.shortlisted_suppliers[spaceId].proposal_name;
                    data.inv_id = $scope.campaignData.shortlisted_inventories[invId].inventory_id;
                    data.inv_type = $scope.campaignData.shortlisted_inventories[invId].inventory_name;
                    data.act_name = $scope.campaignData.inventory_activities[actId].activity_type;
                    data.act_date = $scope.campaignData.inventory_activity_assignment[assignId].activity_date;
                    data.assigned_to = $scope.campaignData.inventory_activity_assignment[assignId].assigned_to;
                    data.reAssign_date = $scope.campaignData.inventory_activity_assignment[assignId].reassigned_activity_date;
                    angular.forEach($scope.campaignData.images, function(images,imgKey){
                      if($scope.campaignData.images[imgKey].inventory_activity_assignment_id == assignId){
                        data.images.push($scope.campaignData.images[imgKey]);
                      }
                    });
                    // data.reAssigner_user = $scope.campaignData.inventory_activity_assignment[assignId].assigned_to;
                    $scope.campaignDataList.push(data);
                  }
                });
              }
            });
          }
        });
      });
    } // end of createList() function

    $scope.setImageUrl = function(images){
      $scope.imageUrlList = [];
      for(var i=0; i<images.length; i++){
        var imageData = {
          image_url : 'http://androidtokyo.s3.amazonaws.com/' + images[i].image_path,
          comment : images[i].comment,
        };
        $scope.imageUrlList.push(imageData);
      }
    }

    $scope.getAllCampaignsForDisplay = function(){
      var campaignsAll = [];
      campaignsAll = $scope.campaignData.completed_campaigns.concat($scope.campaignData.upcoming_campaigns,$scope.campaignData.ongoing_campaigns);

      return campaignsAll;
    }
    $scope.getSelectedText = function() {
        if ($scope.selectedItem.value !== undefined) {
          $scope.getCampaignDetails($scope.selectedItem.value.proposal_id,'supplier_code');
          return $scope.selectedItem.value.name;
        } else {
          return "Please select a campaign";
        }
      };
})
