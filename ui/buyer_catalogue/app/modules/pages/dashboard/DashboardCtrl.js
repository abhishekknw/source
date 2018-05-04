/**
 * @author v.lugovksy
 * created on 16.12.2015
 */
(function () {
    'use strict';

  angular.module('catalogueApp')
      .controller('DashboardCtrl',function($scope, $rootScope, baConfig, colorHelper,DashboardService, commonDataShare, constants) {
 $scope.itemsByPage=15;
 $scope.query = "";

 $scope.rowCollection = [];
        $scope.invKeys = [
          {header : 'POSTER'},
          {header : 'STANDEE'},
          {header : 'STALL'},
          {header : 'FLIER'},
        ];
        $scope.actKeys = [
          {header : 'RELEASE', key : 'release'},
          {header : 'AUDIT', key : 'audit'},
          {header : 'CLOSURE', key : 'closure'},
        ];
        $scope.supHeaders = [
          {header : 'Campaign Name', key : 'proposal_name'},
          {header : 'Supplier Name', key : 'supplier_name'},
          {header : 'Inventory Name', key : 'inv_type'},
          {header : 'Activity Name', key : 'act_name'},
          {header : 'Images', key : ''},
        ];
        $scope.campaignStatus = {
          ongoing : {
            status : 'ongoing', value : false, campaignLabel : 'Ongoing Campaigns', supplierLabel : 'Ongoing Suppliers'
          },
          completed : {
            status : 'completed', value : false, campaignLabel : 'Completed Campaigns', supplierLabel : 'Completed Suppliers'
          },
          upcoming : {
            status : 'upcoming', value : false, campaignLabel : 'Upcoming Campaigns', supplierLabel : 'Upcoming Suppliers'
          },
        };
        $scope.charts = {
          bar : { name : 'Bar Chart', value : 'bar' },
          pie : { name : 'Pie Chart', value : 'pie' },
          doughnut : { name : 'Doughnut Chart', value : 'doughnut' },
          // polarArea : { name : 'PolarArea Chart', value : 'polarArea' },
          // HorizontalBar : { name : 'horizontalBar Chart', value : 'horizontalBar' },
        };
        $scope.perfMetrics = {
          inv : 'inv',
          ontime : 'onTime',
          location : 'onLocation'
        };
        $scope.showPerfMetrics = false;
       $scope.perfPanel = {
          all : 'all',
          respective : 'respective'
          };
        $scope.showPerfPanel = false;
        $scope.inventories = constants.inventories;
        $scope.campaignStatusLabels = [$scope.campaignStatus.ongoing.name,$scope.campaignStatus.completed.name, $scope.campaignStatus.upcoming.name];
        $scope.pieChartDefaulOptions = { legend: { display: true, position: 'right',padding: '10px' } };
        $scope.getCampaignsMenu = function(status){
          $scope.campaignStatus.ongoing.value = false;
          $scope.campaignStatus.completed.value = false;
          $scope.campaignStatus.upcoming.value = false;
          $scope.campaignStatus[status].value = !$scope.campaignStatus[status].value;
          console.log($scope.campaignStatus[status].value);
        }

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

        var category = $rootScope.globals.userInfo.profile.organisation.category;
        var orgId = $rootScope.globals.userInfo.profile.organisation.organisation_id;
        $scope.campaignDataList = [];
        var getAllCampaignsData = function(){
          DashboardService.getAllCampaignsData(orgId, category)
          .then(function onSuccess(response){
            console.log(response);
            $scope.count = 0;
            $scope.invActDateList = [];
            $scope.inventoryActivityCountData = response.data.data;
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

        var loadData = function(){
            getAllCampaignsData();
        }
        loadData();

        function sortObject(obj) {
          return Object.keys(obj).sort().reverse().reduce(function (result, key) {
              result[key] = obj[key];
              return result;
          }, {});
        }

        $scope.count = 0;
        $scope.getDate = function(count){
          console.log(count);
          $scope.date =  $scope.invActDateList[count];
          console.log($scope.date);
        }

        $scope.getPercent = function(num1,num2){
          var percent = num1/num2*100;
          return percent;
        }

        $scope.getAssignedIdsAndImages = function(date,type,inventory){
          console.log(date,type,inventory);
          $scope.showAssignedInvTable = true;
          DashboardService.getAssignedIdsAndImages(orgId, category, type, date, inventory)
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

        $scope.getCampaigns = function(date){
            $scope.showSupplierTypeCountChart = false;
          if(!date)
            date = new Date();
          date = commonDataShare.formatDate(date);
          date = date + ' 00:00:00';

          console.log(date);
          DashboardService.getCampaigns(orgId, category, date)
          .then(function onSuccess(response){
            console.log(response);
            $scope.campaignData = response.data.data;

            $scope.campaigns = [$scope.campaignData.ongoing_campaigns.length,$scope.campaignData.completed_campaigns.length,$scope.campaignData.upcoming_campaigns.length];
            $scope.campaignChartdata = [
              { label : $scope.campaignStatus.ongoing.campaignLabel, value : $scope.campaignData.ongoing_campaigns.length },
              { label : $scope.campaignStatus.completed.campaignLabel, value : $scope.campaignData.completed_campaigns.length },
              { label : $scope.campaignStatus.upcoming.campaignLabel, value : $scope.campaignData.upcoming_campaigns.length }
            ];
            $scope.options = angular.copy(doughnutChartOptions);
            $scope.options.chart.pie.dispatch['elementClick'] = function(e){ $scope.pieChartClick(e.data.label); };
            // $scope.getCampaignsByStatus($scope.campaignStatus.all_campaigns.value);
            console.log($scope.campaignLength);
            $scope.showPerfPanel = $scope.perfPanel.all;
          }).catch(function onError(response){
            console.log(response);
          })
        }


      $scope.pieChartClick = function(label){
        $scope.campaignStatusName = label;
        var campaignStatus = _.findKey($scope.campaignStatus, {'campaignLabel' : label});
        console.log(campaignStatus);
        getCountOfSupplierTypesByCampaignStatus(campaignStatus);
      }
       var getCountOfSupplierTypesByCampaignStatus = function(campaignStatus){
         DashboardService.getCountOfSupplierTypesByCampaignStatus(campaignStatus)
         .then(function onSuccess(response){
           console.log(response);
           if(response.data.data){

              $scope.supplierCodeCountData = formatCountData(response.data.data);

              // $scope.supplierCodeLabelData = formatLabelData(response.data.data.supplier_code_data,'supplier_type_code');
              $scope.supplierCodeCountOptions = angular.copy(doughnutChartOptions);
              $scope.supplierCodeCountOptions.chart.tooltip['contentGenerator'] = function(e){ return getTooltipData(e); };
              $scope.showSupplierTypeCountChart = true;
           }

         }).catch(function onError(response){
           console.log(response);
         })
       }

       var formatCountData = function(data){
         var countData = [];
         angular.forEach(data, function(items,key){
           var temp_data = {
             label : constants[key] + ' Campaigns',
             value : items.length,
             campaigns : items
           }
           countData.push(temp_data);
         })
         return countData;
       }
       var formatSupplierCountData = function(data){
         var countData = [];
         angular.forEach(data, function(item){
           var temp_data = {
             label : constants[item.supplier_code] + ' Count',
             value : item.total,
           }
           countData.push(temp_data);
         })
         return countData;
       }

       var formatLabelData = function(data,label){
         var labelData = [];
         angular.forEach(data, function(item){
           labelData.push(item[label]);
         })
         return labelData;
       }
       $scope.type = $scope.charts.doughnut.value;
       $scope.series = ["Campaigns"];
       $scope.getChart = function(chartType){
         $scope.data = [$scope.campaigns];
         console.log(chartType);
         if(chartType == 'doughnut'){
           $scope.options = angular.copy(doughnutChartOptions);
           $scope.options.chart.pie.dispatch['elementClick'] = function(e){ $scope.pieChartClick(e.data.label); };
         }
         if(chartType == 'pie'){
           $scope.options = $scope.pieChartOptions;
         }
         if(chartType == 'bar'){

           $scope.options = $scope.barChartOptions;
         }
         // if(chartType == 'bar')
         //    $scope.campaigns = [$scope.campaigns];
         $scope.type = chartType;
       }

       var doughnutChartOptions = {
            chart: {
                type: 'pieChart',
                height: 350,
                donut: true,
                x: function(d){return d.label;},
                y: function(d){return d.value;},

                showLabels: true,
                labelType : 'value',
                pie: {
                    startAngle: function(d) { return d.startAngle -Math.PI/2 },
                    endAngle: function(d) { return d.endAngle -Math.PI/2 },
                    dispatch : {
                    }
                },
                duration: 500,
                legend: {
                  rightAlign:true,
                    margin: {
                        top: 5,
                        right: 70,
                        bottom: 5,
                        left: 0
                    }
                },
                legendPosition : 'right',
                tooltip: {
              },
              interactive : true
            }
        };
        $scope.pieChartOptions = {
           chart: {
               type: 'pieChart',
               height: 350,
               x: function(d){return d.label;},
               y: function(d){return d.value;},
               showLabels: true,
               labelType : 'value',
               duration: 500,
               labelThreshold: 0.01,
               labelSunbeamLayout: true,
               legend: {
                   margin: {
                       top: 5,
                       right: 35,
                       bottom: 5,
                       left: 0
                   }
               },
               legendPosition : 'right',
           }
       };
       $scope.barChartOptions = {
           chart: {
               type: 'discreteBarChart',
               height: 350,
               margin : {
                   top: 20,
                   right: 20,
                   bottom: 50,
                   left: 55
               },
               x: function(d){return d.label;},
               y: function(d){return d.value + (1e-10);},
               showValues: true,
               // valueFormat: function(d){
               //     return d3.format(',.4f')(d);
               // },
               duration: 500,
               xAxis: {
                   axisLabel: 'X Axis'
               },
               yAxis: {
                   axisLabel: 'Y Axis',
                   axisLabelDistance: -10
               }
           }
       };

       // START : service call to get suppliers as campaign status
       $scope.getSuppliersOfCampaignWithStatus = function(campaignId){
         DashboardService.getSuppliersOfCampaignWithStatus(campaignId)
         .then(function onSuccess(response){
           console.log(response);
           $scope.campaignStatusData = response.data.data;
           $scope.campaignChartdata = [
             { label : $scope.campaignStatus.ongoing.supplierLabel, value : $scope.campaignStatusData.ongoing.length },
             { label : $scope.campaignStatus.completed.supplierLabel, value : $scope.campaignStatusData.completed.length },
             { label : $scope.campaignStatus.upcoming.supplierLabel, value : $scope.campaignStatusData.upcoming.length }
           ];
           $scope.options = angular.copy(doughnutChartOptions);
         }).catch(function onError(response){
           console.log(response);
         })
       }
       // END : service call to get suppliers as campaign status

       // START : get campaign filters
       $scope.getCampaignFilters = function(campaignId){
         $scope.campaignId = campaignId;
         DashboardService.getCampaignFilters(campaignId)
         .then(function onSuccess(response){
           console.log(response);
           $scope.campaignInventories = response.data.data;
         }).catch(function onError(response){
           console.log(response);
         })
       }
       // END : get campaign filters

       // START : get Performance metrics data
       $scope.getPerformanceMetricsData = function(inv){
         $scope.inv = inv;
         DashboardService.getPerformanceMetricsData($scope.campaignId,inv)
         .then(function onSuccess(response){
           $scope.performanceMetricsData = response.data.data;
           $scope.showPerfMetrics = $scope.perfMetrics.inv;
           setOntimeData($scope.performanceMetricsData);
         }).catch(function onError(response){
           console.log(response);
         })
       }
       // END : get Performance metrics data

       // START : create on time data on activities
        var setOntimeData = function(data){
          angular.forEach(data, function(activity){
            activity['ontime'] = 0;
            for(var i=0;i<activity['actual'].length;i++){
              var days = Math.floor((new Date(activity.actual[i].created_at) - new Date(activity.actual[i].actual_activity_date)) / (1000 * 60 * 60 * 24));
              if(days == 0){
                activity['ontime'] += 1;
              }
              console.log(days);
            }
          })
          console.log(data);
        }
       // END : create on time data on activities
       $scope.getOnTimeData = function(){
         $scope.showPerfMetrics = $scope.perfMetrics.ontime;
       }

       $scope.getLocationData = function(){
         DashboardService.getLocationData($scope.campaignId,$scope.inv)
         .then(function onSuccess(response){
           console.log(response);
           $scope.locationData = response.data.data;
           getOnLocationData($scope.locationData);
           $scope.showPerfMetrics = $scope.perfMetrics.onlocation;
         }).catch(function onError(response){
           console.log(response);
         })
       }
       var getOnLocationData = function(data){
         $scope.onLocation = 0;
         $scope.onLocationData = {
           [constants.release] : {
             actual : [],
             total : 0
           },
           [constants.audit] : {
             actual : [],
             total : 0
           },
           [constants.closure] : {
             actual : [],
             total : 0
           }
         };
         angular.forEach(data, function(items,key){
           console.log(key,Object.keys(items).length);

           $scope.onLocationData[key].total = Object.keys(items).length;
             angular.forEach(items, function(activities,id){
               for(var i=0; i<activities.length; i++){
                 if(activities[i].hasOwnProperty('distance') && activities[i].distance <= constants.distanceLimit){
                   $scope.onLocationData[key].actual.push(activities[i]);
                 }
               }
             })
         })
         console.log($scope.onLocationData);
       }
       $scope.initializePerfMetrix = function(){
         $scope.showSupplierTypeCountChart = false;
       }
       var getTooltipData = function(e){
         console.log(e);

         var rows = [];
         var count = 0;
          angular.forEach(e.data.campaigns, function(campaign){
            count++;
            rows= rows +
            "<tr>" +
              "<td class='key'>" + count  + "</td>" +
              "<td class='key'>" + campaign.proposal__name + "</td>" +
              "<td class='x-value'>" + constants[campaign.supplier_code] + "</td>" +
              "<td class='x-value'>" + campaign.total + "</td>" +
            "</tr>"
          })

                 var header =
                   "<thead>" +
                   "<tr>" +
                       "<td class='legend-color-guide'><div style='background-color: " + e.color + ";'></div></td>" +
                       "<td class='key'><strong>" + e.data.label + "</strong></td>" +
                     "</tr>" +
                     "<tr>" +
                       "<td class='key'><strong>" + 'Index' + "</strong></td>" +
                       "<td class='key'><strong>" + 'Campaign Name' + "</strong></td>" +
                       "<td class='key'><strong>" + 'Supplier Name' + "</strong></td>" +
                       "<td class='key'><strong>" + 'Total Count' + "</strong></td>" +                       
                     "</tr>" +
                   "</thead>";

                 return "<table>" +
                     header +
                     "<tbody>" +
                       rows +
                     "</tbody>" +
                   "</table>";

       }
    })
  })();
