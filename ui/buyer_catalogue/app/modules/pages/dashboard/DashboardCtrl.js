/**
 * @author v.lugovksy
 * created on 16.12.2015
 */
(function () {
    'use strict';

  angular.module('catalogueApp')
      .controller('DashboardCtrl',function($scope, $rootScope, baConfig, colorHelper,DashboardService, commonDataShare, constants,$location,$anchorScroll) {
 $scope.itemsByPage=15;
 $scope.query = "";
 $scope.oneAtATime = true;

 $scope.rowCollection = [];
        $scope.invKeys = [
          {header : 'POSTER'},
          {header : 'STANDEE'},
          {header : 'STALL'},
          {header : 'FLIER'},
          {header : 'GATEWAY ARCH'},
        ];
        $scope.invCodes = {
          PO : 'PO',
          ST : 'ST',
          SL : 'SL',
          FL : 'FL',
          GA : 'GA'
        };
        $scope.actKeys = [
          {header : 'RELEASE', key : 'release', label1 : 'Released', label2 : 'UnReleased'},
          {header : 'AUDIT', key : 'audit', label1 : 'Audited', label2 : 'UnAudited'},
          {header : 'CLOSURE', key : 'closure', label1 : 'Closed', label2 : 'UnClosed' },
        ];


        $scope.supHeaders = [
          {header : 'Campaign Name', key : 'proposal_name'},
          {header : 'Inventory', key : 'supplier_name'},
          {header : 'Today Released', key : 'inv_type'},
          {header : 'Average Delay(%)', key : 'act_name'},
          {header : 'Average Off Location(Meters)', key : 'act_name'},
          {header : 'Images', key : 'images'},
        ];
        $scope.campaignStatus = {
          ongoing : {
            status : 'ongoing', value : false, campaignLabel : 'Ongoing Campaigns', supplierLabel : 'Ongoing Societies'
          },
          completed : {
            status : 'completed', value : false, campaignLabel : 'Completed Campaigns', supplierLabel : 'Completed Societies'
          },
          upcoming : {
            status : 'upcoming', value : false, campaignLabel : 'Upcoming Campaigns', supplierLabel : 'Upcoming Societies'
          },
        };
        $scope.charts = {
          pie : { name : 'Pie Chart', value : 'pie' },
          doughnut : { name : 'Doughnut Chart', value : 'doughnut' },

        };
        $scope.LeadsHeader = [
          {header : 'Ongoing'},
          {header : 'Completed'},

        ];
        $scope.perfLeads = {
          all : 'all',
          invleads : 'invleads',
        };
        $scope.showPerfLeads = false;

        $scope.perfMetrics = {
          inv : 'inv',
          ontime : 'onTime',
          location : 'onLocation',
          leads : 'leads',
          multipleLeads : 'multipleLeads',
          blank : 'blank'
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
            $scope.loading = response.data.data;
            console.log(response);
            $scope.count = 0;
            $scope.invActDateList = [];
            $scope.inventoryActivityCountData = response.data.data;
            console.log($scope.inventoryActivityCountData);
            angular.forEach(response.data.data, function(data,key){
              $scope.isPanelOpen = !$scope.isPanelOpen;
              $scope.inventoryActivityCountData[key] = sortObject(data);
              console.log($scope.inventoryActivityCountData[key]);
              $scope.invActDateList = $scope.invActDateList.concat(Object.keys($scope.inventoryActivityCountData[key]));
            })
            $scope.invActDateList = Array.from(new Set($scope.invActDateList));
            $scope.invActDateList.sort().reverse();
            $scope.dateListKeys = {};
            angular.forEach($scope.invActDateList, function(date){
              $scope.dateListKeys[date] = date;
            })
            getHistory(response.data.data);

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
        $scope.date = new Date();
        $scope.pre = -1;
        $scope.next = 1;
        $scope.getDate = function(day){

          $scope.showAssignedInvTable = false;
          $scope.OntimeOnlocation.ontime.value = false;
          $scope.OntimeOnlocation.onlocation.value = false;
          $scope.date = new Date($scope.date);
          $scope.date.setDate($scope.date.getDate() + day);
          $scope.date = commonDataShare.formatDate($scope.date);
          console.log($scope.dateListKeys);
          // $scope.date =  $scope.invActDateList[count];
        }
        $scope.getRecentActivity = function(day){
          console.log(day);
          $scope.isPanelOpen =!$scope.isPanelOpen;
          $scope.showAssignedInvTable = false;
          $scope.OntimeOnlocation.ontime.value = false;
          $scope.OntimeOnlocation.onlocation.value = false;
          var initialDate = $scope.date;
          var date = new Date($scope.date);
          var counter = 100000;
          date.setDate(date.getDate() + day);
          date = commonDataShare.formatDate(date);

          while($scope.dateListKeys[date] != date){
            date = new Date(date);
            date.setDate(date.getDate() + day);
            date = commonDataShare.formatDate(date);
            counter--;
            if(counter < 0){
              alert("No Activity");
              break;
            }
            // console.log("ji",date,counter);
          }
          if(counter < 0)
            $scope.date = initialDate;
          else
            $scope.date = date;
        }

        $scope.getPercent = function(num1,num2){
          var percent = num1/num2*100;
          return percent;
        }

        $scope.getAssignedIdsAndImages = function(date,type,inventory){

          console.log(date,type,inventory);
          $scope.invName = inventory;
          $scope.actType = type;
          DashboardService.getAssignedIdsAndImages(orgId, category, type, date, inventory)
          .then(function onSuccess(response){
            console.log(response);
            $scope.campaignReleaseData = [];
            var campaignReleaseData = [];

            campaignReleaseData['totalOnTimeCount'] = 0;
            campaignReleaseData['totalOffTimeCount'] = 0;
            campaignReleaseData['totalOnLocationCount'] = 0;
            campaignReleaseData['totalOffLocationCount'] = 0;
            campaignReleaseData['totalOffLocationDistance'] = 0;
            campaignReleaseData['totalOffTimeDays'] = 0;
            campaignReleaseData['totalInvCount'] = 0;

            angular.forEach(response.data.data, function(data,campaignName){
              console.log(data);
              $scope.campaignData = [];
              var campaignData = {};
              console.log(campaignData);
              campaignData['name'] = campaignName;
              campaignData['images'] = [];
              campaignData['inv_count'] = 0;
              campaignData['onLocationCount'] = 0;
              campaignData['offLocationCount'] = 0;
              campaignData['onTimeCount'] = 0;
              campaignData['offTimeCount'] = 0;
              campaignData['offTimeDays'] = 0;
              campaignData['offLocationDistance'] = 0;
              angular.forEach(data, function(items,inv){
                campaignData.inv_count += 1;
                campaignData[inv] = {};
                console.log(items);
                campaignData[inv]['onLocation'] = false;
                campaignData[inv]['onTime'] = false;
                campaignData[inv]['minDistance'] = 100;
                campaignData[inv]['dayCount'] = 100;

                  for(var i=0; i<items.length; i++){
                    campaignData['proposalId'] = items[i].proposal_id;
                    if(items[i].hasOwnProperty('distance') && items[i].distance <= constants.distanceLimit){
                      campaignData[inv]['onLocation'] = true;
                      campaignData[inv]['minDistance'] = items[i].distance;
                      break;
                    }
                    else if(items[i].hasOwnProperty('distance')){
                      if(items[i].distance < campaignData[inv]['minDistance']){
                        campaignData[inv]['minDistance'] = items[i].distance;
                      }
                    }
                  }
                  //onTime
                  for(var i=0; i<items.length; i++){
                    console.log(items);
                    var days = Math.floor((new Date(items[i].created_at) - new Date(items[i].actual_activity_date)) / (1000 * 60 * 60 * 24));
                    if(days == 0){
                      campaignData[inv]['onTime'] = true;
                      break;
                    }else if(days < campaignData[inv]['dayCount']){
                      campaignData[inv]['dayCount'] = days;
                    }
                  }
                  if(campaignData[inv]['onLocation']){
                    campaignData['onLocationCount'] += 1;
                    campaignData['offLocationDistance'] += campaignData[inv]['minDistance'];
                  }
                  else{
                    campaignData['offLocationCount'] += 1;
                    campaignData['offLocationDistance'] += campaignData[inv]['minDistance'];
                  }


                  if(campaignData[inv]['onTime'])
                    campaignData['onTimeCount'] += 1;
                  else{
                    campaignData['offTimeCount'] += 1;
                    campaignData['offTimeDays'] += campaignData[inv]['dayCount'];
                  }
                  campaignData['images'].push(items);

              })
              campaignReleaseData['totalOnTimeCount'] += campaignData['onTimeCount'];
              campaignReleaseData['totalOffTimeCount'] += campaignData['offTimeCount'];
              campaignReleaseData['totalOnLocationCount'] += campaignData['onLocationCount'];
              campaignReleaseData['totalOffLocationCount'] += campaignData['offLocationCount'];
              campaignReleaseData['totalOffLocationDistance'] += campaignData['offLocationDistance'];
              campaignReleaseData['totalInvCount'] += campaignData['inv_count'];
              campaignReleaseData['totalOffTimeDays'] += campaignData['offTimeDays'];

              campaignReleaseData.push(campaignData);
            })
            $scope.campaignReleaseData = campaignReleaseData;
            console.log($scope.campaignReleaseData);
            if($scope.campaignReleaseData.length){
                $scope.showAssignedInvTable = true;
            }else{
                $scope.showAssignedInvTable = false;
            }
            $scope.campaignDataList = [];
            // createList();
            console.log(  $scope.campaignDataList);
            console.log($scope.campaignReleaseData);
          }).catch(function onError(response){
            console.log(response);
          })
        }

        $scope.goToExecutionPage = function(images){
          $scope.imageUrlList = [];
          angular.forEach(images, function(imageObjects){
            for(var i=0; i<imageObjects.length; i++){
              var imageData = {
                image_url : 'http://androidtokyo.s3.amazonaws.com/' + imageObjects[i].image_path,
                comment : imageObjects[i].comment,
              };
              $scope.imageUrlList.push(imageData);
            }
          })

        }

        $scope.getCampaigns = function(date){
            $scope.showSupplierTypeCountChart = false;
          if(!date)
            date = new Date();
          date = commonDataShare.formatDate(date);
          date = date + ' 00:00:00';
          $scope.showCampaignGraph = true;
          $scope.showLeadsDetails = false;
          $scope.showLeadsDetailsDataTable = false;

          console.log(date);
          DashboardService.getCampaigns(orgId, category, date)
          .then(function onSuccess(response){
            console.log(response);
            $scope.loading = response.data.data;
            $scope.searchSelectAllModel = [];
            console.log($scope.searchSelectAllModel);
            angular.forEach($scope.searchSelectAllModel, function(data){
              $scope.modelData = $scope.searchSelectAllModel;
              console.log($scope.modelData);
            })
            $scope.campaignData = response.data.data;
            console.log($scope.campaignData);

            $scope.mergedarray = [];
            // $scope.mergedarray.push.apply($scope.campaignData.ongoing_campaigns,$scope.campaignData.completed_campaigns,$scope.campaignData.upcoming_campaigns);
            angular.forEach($scope.campaignData, function(data){
              console.log($scope.campaignData);

              console.log(data);
              angular.forEach(data,function(campaign){
                  $scope.mergedarray.push(campaign);
              })

          })
            $scope.campaigns = [$scope.campaignData.ongoing_campaigns.length,$scope.campaignData.completed_campaigns.length,$scope.campaignData.upcoming_campaigns.length];
            console.log($scope.campaignData);

              $scope.campaignChartdata = [
              { label : $scope.campaignStatus.ongoing.campaignLabel, value : $scope.campaignData.ongoing_campaigns.length },
              { label : $scope.campaignStatus.completed.campaignLabel, value : $scope.campaignData.completed_campaigns.length },
              { label : $scope.campaignStatus.upcoming.campaignLabel, value : $scope.campaignData.upcoming_campaigns.length }
            ];
            console.log(  $scope.campaignChartdata );
            $scope.options = angular.copy(doughnutChartOptions);
            $scope.options.chart.pie.dispatch['elementClick'] = function(e){ $scope.pieChartClick(e.data.label); };
            $scope.options.chart.pie.dispatch['elementClick'] = function(e){ $scope.getDisplayDetailsTable(e.data); };

            // $scope.getCampaignsByStatus($scope.campaignStatus.all_campaigns.value);
            console.log($scope.campaignLength);
            $scope.showPerfPanel = $scope.perfPanel.all;
          }).catch(function onError(response){
            console.log(response);
          })
        }


      $scope.pieChartClick = function(label){

        $anchorScroll('bottom');
        console.log("hi");

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
              console.log($scope.supplierCodeCountData );

              // $scope.supplierCodeLabelData = formatLabelData(response.data.data.supplier_code_data,'supplier_type_code');
              $scope.supplierCodeCountOptions = angular.copy(doughnutChartOptions);

              // $scope.supplierCodeCountOptions.chart.tooltip['contentGenerator'] = function(e){ return getTooltipData(e); };
              $scope.supplierCodeCountOptions.chart.pie.dispatch['elementClick'] = function(e){ $scope.getCampaignInvTableData(e.data); };

              $scope.showSupplierTypeCountChart = true;

           }

         }).catch(function onError(response){
           console.log(response);
         })
       }


          $scope.doughnutChartOptions = function(){
               $anchorScroll('bottom');
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
           $scope.options.chart.pie.dispatch['elementClick'] = function(e){
             $scope.pieChartClick(e.data.label);


            };

         }
         if(chartType == 'pie'){
           $scope.options = $scope.pieChartOptions;
         }
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
                  rightAlign:false,
                    // margin: {
                    //     top: 5,
                    //     right: 100,
                    //     bottom: 5,
                    //     left: 0
                    // },
                },
                legendPosition : 'bottom',
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
                 rightAlign:false,
                   // margin: {
                   //     top: 5,
                   //     right: 35,
                   //     bottom: 5,
                   //     left: 0
                   // }
               },
               legendPosition : 'bottom',
           }
       };

       var stackedBarChart = {
          "chart": {
            "type": "multiBarChart",
            "height": 450,
            // "labelType" : "11",
            "margin": {
              "top": 100,
              "right": 20,
              "bottom": 145,
              "left": 45
            },
            "clipEdge": true,
            "duration": 500,
            "stacked": true,
              "xAxis": {
              "axisLabel": "",
              "showMaxMin": false,
              "rotateLabels" : -30
            },
            "yAxis": {
              "axisLabel": "",
              "axisLabelDistance": -20,

              "ticks" : 8
            },
            "legend" : {
                    "margin": {
                    "top": 5,
                    "right": 3,
                    "bottom": 5,
                    "left": 15
                },
            },

            "reduceXTicks" : false
          }
        };

        var lineChart = {
          "chart": {
            "type": "lineChart",
            "height": 450,
            "useInteractiveGuideline": true,
            "dispatch": {},
            "xAxis": {
              "axisLabel": "Campaigns",
              tickFormat: function(d) {
                console.log(d);
                return d.y;
              }
            },
            "yAxis": {
              "axisLabel": "",
            }
          }
        };


       // START : service call to get suppliers as campaign status
       $scope.getSuppliersOfCampaignWithStatus = function(campaignId){
         getCampaignInventoryActivitydetails(campaignId);
         $scope.getCampaignFilters(campaignId);
         DashboardService.getSuppliersOfCampaignWithStatus(campaignId)
         .then(function onSuccess(response){

           console.log(response);
           $scope.showLeadsDetails = false;
           $scope.showLeadsDetailsDataTable = false;
           $scope.showSupplierTypeCountChart = false;
           $scope.showCampaignInvTable = false;
           $scope.showSupplierInvTable = false;
           $scope.showSingleCampaignChart = true;


           for(var i=0;i<$scope.campaignInventories.length;i++){
              if($scope.campaignInventories[i].filter_code=='SL'){
                  $scope.showLeadsDetails = true;
                   $scope.showLeadsDetailsDataTable = true;
                  }
         }

           $scope.campaignStatusData = response.data.data;
           $scope.campaignSupplierAndInvData = response.data.data;
           $scope.showSupplierSocietywiseInvTable = false;
           $scope.showSupplierInvdDataTable = function(invData){
             $scope.SocietyInvTable = $scope.campaignStatusData;
             $scope.showSupplierSocietywiseInvTable = true;
           };
           $scope.countallsupplier = $scope.campaignStatusData.completed.length+$scope.campaignStatusData.ongoing.length+$scope.campaignStatusData.upcoming.length;
           // console.log($scope.countallsupplier);
           var totalFlats=0,totalLeads=0,totalSuppliers=0,hotLeads=0;
           console.log($scope.campaignStatusData);

           // $scope.totalLeadsCount = response.data.data.supplier_data.length;
           $scope.campaignStatusData['totalSuppliers'] = 0;
           angular.forEach($scope.campaignStatusData, function(data,key){
              if($scope.campaignStatusData[key].length){
                console.log($scope.campaignStatusData[key].length);
                $scope.campaignStatusData[key]['totalFlats'] = 0;
                $scope.campaignStatusData[key]['totalLeads'] = 0;
                $scope.campaignStatusData[key]['hotLeads'] = 0;
                $scope.campaignStatusData['totalSuppliers'] += $scope.campaignStatusData[key].length;
                angular.forEach(data, function(supplierData){
                  $scope.campaignStatusData[key]['totalFlats'] += supplierData.supplier.flat_count;
                  $scope.campaignStatusData[key]['totalLeads'] += supplierData.leads_data.length;
                  if(supplierData.leads_data.length){
                    angular.forEach(supplierData.leads_data, function(lead) {
                      if(lead.is_interested){
                        $scope.campaignStatusData[key]['hotLeads'] += 1;

                      }
                    })
                  }
                })
                totalLeads += $scope.campaignStatusData[key].totalLeads;
                totalFlats += $scope.campaignStatusData[key].totalFlats;
                // totalSuppliers += $scope.campaignStatusData.totalSuppliers;
              }
         })
            $scope.avgLeadsPerFlat = totalLeads/totalFlats * 100;
            $scope.avgLeadsPerSupplier = totalLeads/$scope.campaignStatusData.totalSuppliers * 100;
            $scope.avgHotLeadsPerFlat = hotLeads/totalFlats * 100;
              $scope.avgHotLeadsPerSupplier = hotLeads/$scope.campaignStatusData.totalSuppliers * 100;
           // console.log($scope.campaignStatusData);

           $scope.campaignChartdata = [
             { label : $scope.campaignStatus.ongoing.supplierLabel, value : $scope.campaignStatusData.ongoing.length, status : $scope.campaignStatus.ongoing.status },
             { label : $scope.campaignStatus.completed.supplierLabel, value : $scope.campaignStatusData.completed.length, status : $scope.campaignStatus.completed.status },
             { label : $scope.campaignStatus.upcoming.supplierLabel, value : $scope.campaignStatusData.upcoming.length, status : $scope.campaignStatus.upcoming.status }
           ];
           $scope.options1 = angular.copy(doughnutChartOptions);
           console.log("hello");
           $scope.options1.chart.pie.dispatch['elementClick'] = function(e){ $scope.getSupplierAndInvData(e.data); };


         }).catch(function onError(response){
           console.log(response);
         })
       }
       // END : service call to get suppliers as campaign status

       $scope.getDisplayDetailsTable = function(campaign){
         $scope.data = $scope.campaignStatusData;
         angular.forEach($scope.campaignStatusData, function(data,key){
           console.log(data);
            if($scope.campaignStatusData[key].length){
              console.log($scope.campaignStatusData[key].length);
              // $scope.data[key]['InvCount'] = 0;
              angular.forEach($scope.campaignStatusData, function(supplierData){
                // $scope.SupplierData = supplierData.supplier;
              console.log(supplierData);
              })

            }
       })

       $scope.showDisplayDetailsTable = true;
         $scope.$apply();
         // console.log($scope.campaignInvData);
      }
       // START : get campaign filters
       $scope.getCampaignFilters = function(campaignId){
         $scope.showTimeLocBtn = false;
         $scope.campaignId = campaignId;
         $scope.showPerfMetrics = $scope.perfMetrics.blank;
         DashboardService.getCampaignFilters(campaignId)
         .then(function onSuccess(response){
           console.log(response);
           // $scope.loading = response.data.data;

           $scope.campaignInventories = [];
           $scope.showinv = true;
           $scope.select = {
            campaignInventories: ""
          };
           angular.forEach(response.data.data, function(inv){
             if($scope.invCodes.hasOwnProperty(inv.filter_code)){
               $scope.campaignInventories.push(inv);
             }
           })
           $scope.performanceMetricsData = [];
           // if($scope.campaignInventories.length){
           //   // $scope.showPerfMetrics = $scope.perfMetrics.inv;
           // }
           // $scope.campaignInventories = response.data.data;
           console.log($scope.campaignInventories);

         }).catch(function onError(response){
           console.log(response);
         })
       }
       // END : get campaign filters

       // START : get Performance metrics data
        $scope.getPerformanceMetricsData = {};
       $scope.getPerformanceMetricsData = function(inv){
         $scope.inv = inv;
         var type = 'inv';
         var perf_param = 'on_time';
         $scope.select.campaignInventories = "";

         // console.log($scope.getPerformanceMetricsData.size);
         DashboardService.getPerformanceMetricsData($scope.campaignId,type,inv,perf_param )
         .then(function onSuccess(response){
           console.log(response);
           $scope.performanceMetricsData = response.data.data;
           $scope.activityInvPerfData = {
             release : Object.keys($scope.performanceMetricsData.actual.release).length,
             audit : Object.keys($scope.performanceMetricsData.actual.audit).length,
             closure : Object.keys($scope.performanceMetricsData.actual.closure).length
           }
           console.log($scope.releaseInvPerfData);
           $scope.showPerfMetrics = $scope.perfMetrics.inv;
           $scope.showTimeLocBtn = true;
           setOntimeData($scope.performanceMetricsData.actual);
         }).catch(function onError(response){
           console.log(response);
         })
       }
       // END : get Performance metrics data

       // START : create on time data on activities
        var setOntimeData = function(data){
          angular.forEach(data, function(activity,key){
            console.log(activity,key);
            activity['ontime'] = 0;
            angular.forEach(activity, function(imageData){
              for(var i=0;i<imageData.length;i++){
                var days = Math.floor((new Date(imageData[i].created_at) - new Date(imageData[i].activity_date)) / (1000 * 60 * 60 * 24));
                if(days == 0){
                  activity['ontime'] += 1;
                  break;
                }
                console.log(days);
              }
            })

          })
          console.log(data);
        }
       // END : create on time data on activities
       $scope.getOnTimeData = function(){
         $scope.showPerfMetrics = $scope.perfMetrics.ontime;
       }

       $scope.getLocationData = function(){
         var type = 'inv';
         var perf_param = 'on_location';
         DashboardService.getPerformanceMetricsData($scope.campaignId,type,$scope.inv,perf_param)
         .then(function onSuccess(response){
           console.log(response);
           $scope.locationData = response.data.data.actual;
           getOnLocationData($scope.locationData);
           console.log($scope.locationData);
           $scope.showPerfMetrics = $scope.perfMetrics.onlocation;
         }).catch(function onError(response){
           console.log(response);
         })
       }
       var getOnLocationData = function(data){




             angular.forEach(data, function(activity,key){
               data[key]['onLocation'] = 0;
               console.log(activity);
               angular.forEach(activity, function(imageData){
                 for(var i=0; i<imageData.length; i++){
                   console.log(imageData[i].inventory_id);
                   if(imageData[i].hasOwnProperty('distance') && imageData[i].distance <= constants.distanceLimit){
                     data[key].onLocation += 1;
                     break;
                   }
                 }
               })

             })


         console.log(data);
       }
       $scope.initializePerfMetrix = function(){
         $scope.showSupplierTypeCountChart = false;
       }
//        var getTooltipData = function(e){
//          var rows = [];
//          var count = 0;
//           angular.forEach(e.data.campaigns, function(campaign){
//             count++;
//             rows= rows +
//             "<tr>" +
//               "<td class='key'>" + count  + "</td>" +
//               "<td class='key'>" + campaign.proposal__name + "</td>" +
//               "<td class='x-value'>" + constants[campaign.supplier_code] + "</td>" +
//               "<td class='x-value'>" + campaign.total + "</td>" +
// "</tr>"
//           })
//
//                  var header =
//                    "<thead>" +
//                    "<tr>" +
//                        "<td class='legend-color-guide'><div style='background-color: " + e.color + ";'></div></td>" +
//                        "<td class='key'><strong>" + e.data.label + "</strong></td>" +
//                      "</tr>" +
//                      "<tr>" +
//                        "<td class='key'><strong>" + 'Index' + "</strong></td>" +
//                        "<td class='key'><strong>" + 'Campaign Name' + "</strong></td>" +
//                        "<td class='key'><strong>" + 'Supplier Name' + "</strong></td>" +
//                        "<td class='key'><strong>" + 'Total Count' + "</strong></td>" +
//                      "</tr>" +
//                    "</thead>";
//
//                  return "<table>" +
//                      header +
//                      "<tbody>" +
//                        rows +
//                      "</tbody>" +
//                    "</table>";
//
//        }

       $scope.getCampaignInvTableData = function(campaigns){
         console.log($scope.campaigns);
         $scope.campaignInvData = campaigns.campaigns;
         console.log($scope.campaignInvData);
         $scope.showCampaignInvTable = true;
         $scope.$apply();
         // console.log($scope.campaignInvData);

     }



     $scope.getCampaignInvTypesData = function(campaign){
       $scope.proposal_id = campaign.proposal_id;
       $scope.campaignName = campaign.proposal__name;
       DashboardService.getCampaignInvTypesData($scope.proposal_id)
       .then(function onSuccess(response){
         console.log(response);
        $scope.campaignInventoryTypesData = response.data.data;
        $scope.loading = response.data.data;
        // console.log($scope.campaignInventoryTypesData.supplier_data);
        $scope.getSupplierInvTableData($scope.campaignInventoryTypesData);
        $scope.campaignInventoryData = response.data.data;
        console.log($scope.campaignInventoryData);
        $scope.totalTowerCount = 0;
        $scope.totalFlatCount = 0;
        $scope.totalSupplierCount = response.data.data.supplier_data.length;
        angular.forEach(response.data.data.supplier_data, function(data,key){

          $scope.totalTowerCount += data.tower_count;
          $scope.totalFlatCount += data.flat_count;

        })

     }).catch(function onError(response){
       console.log(response);
     })
    }

    $scope.getSupplierInvTableData = function(supplier){
      $scope.supplierInvData = supplier;
      // console.log(  $scope.supplierInvData );
      $scope.showSupplierInvTable = true;

    }

    var getCampaignInventoryActivitydetails = function(campaignId){
    DashboardService.getCampaignInventoryActivitydetails(campaignId)
      .then(function onSuccess(response){
        console.log(response);
        $scope.campaignInventoryActivityData = response.data.data;
        console.log($scope.campaignInventoryActivityData);
        }).catch(function onError(response){
      console.log(response);
    })
   }




     $scope.onLocationDetails = false;
       $scope.onTimeDetails = false;

   $scope.OntimeOnlocation = {
     ontime : {
       status : 'ontime', value : false
     },
     onlocation : {
       status : 'onlocation', value : false
     },
   };

   $scope.showOntimeOnlocation = function(status){
     $scope.showOnClickDetails = true;
     $scope.OntimeOnlocation.ontime.value = false;
     $scope.OntimeOnlocation.onlocation.value = false;

     $scope.OntimeOnlocation[status].value = !$scope.OntimeOnlocation[status].value;
   }


   var getHistory = function(data){
     $scope.historyData = {};
     angular.forEach(data, function(dates,invKey){
       console.log(dates);
       angular.forEach(dates, function(activities,dateKey){
         if(!$scope.historyData.hasOwnProperty(dateKey)){
           $scope.historyData[dateKey] = {};
         }
         angular.forEach(activities, function(count,actKey){
           if(!$scope.historyData[dateKey].hasOwnProperty(actKey)){
             $scope.historyData[dateKey][actKey] = {};
             $scope.historyData[dateKey][actKey]['actual'] = 0;
             $scope.historyData[dateKey][actKey]['total'] = 0;
           }
           $scope.historyData[dateKey][actKey].actual += data[invKey][dateKey][actKey].actual;
           $scope.historyData[dateKey][actKey].total += data[invKey][dateKey][actKey].total;
         })
       })
     })
     console.log($scope.historyData);
   }
   $scope.goToExecutionPage = function(proposalId){
     console.log(proposalId);
     $location.path('/' + proposalId + '/opsExecutionPlan');
   }
   $scope.getLeadsByCampaign = function(campaignId){
     $scope.showTimeLocBtn = false;
     $scope.showinv = false;
     $scope.showPerfMetrics = $scope.perfMetrics.blank;
     DashboardService.getLeadsByCampaign(campaignId)
     .then(function onSuccess(response){
       console.log(response);
       $scope.stackedBarChartOptions = angular.copy(stackedBarChart);
       $scope.stackedBarChartSupplierData = formatMultiBarChartDataForSuppliers(response.data.data.supplier_data);
       $scope.stackedBarChartDateData = formatMultiBarChartDataByDate(response.data.data.date_data);
       $scope.campaignLeadsData = response.data.data;
       $scope.showPerfMetrics = $scope.perfMetrics.leads;
     }).catch(function onError(response){
       console.log(response);
     })
   }
   var formatMultiBarChartDataForSuppliers = function(data){
     var values1 = [];
     var values2 = [];
     angular.forEach(data, function(supplier){
       console.log(supplier);
        var value1 =
           { x : supplier.data.society_name, y : supplier.total - supplier.interested};
        var value2 =
           { x : supplier.data.society_name, y : supplier.interested};
        values1.push(value1);
        values2.push(value2);
     })
     var temp_data = [
       {
         key : "Normal Leads",
         color : constants.colorKey1,
         values : values1
       },
       {
         key : "High Potential Leads",
         color : constants.colorKey2,
         values : values2
       }
     ];
     console.log(temp_data);
     return temp_data;
   }
   var formatMultiBarChartDataByDate = function(data){
     var values1 = [];
     var values2 = [];
     angular.forEach(data, function(date){
       var tempDate = commonDataShare.formatDate(date.created_at);
        var value1 =
           { x : tempDate, y : date.total - date.interested};
        var value2 =
           { x : tempDate, y : date.interested};
        values1.push(value1);
        values2.push(value2);
     })
     var temp_data = [
       {
         key : "Normal Leads",
         color : constants.colorKey1,
         values : values1
       },
       {
         key : "High Potential Leads",
         color : constants.colorKey2,
         values : values2
       }
     ];
     console.log(temp_data);
     return temp_data;
   }


   $scope.getDateData = function(date){
     $scope.date = date;
   }


   $scope.graphicalComparision = {
     leads : {
       status : 'leads', value : false
     },
     inventory : {
       status : 'inventory', value : false
     },
   };
   $scope.getGraphicalComparision = function(status){
     $scope.graphicalComparision.leads.value = false;
     $scope.graphicalComparision.inventory.value = false;
     $scope.showPerfMetrics = false;
     $scope.campaignInventories = [];
     $scope.showTimeLocBtn = false;
     $scope.graphicalComparision[status].value = !$scope.graphicalComparision[status].value;
   }

   $scope.searchSelectAllSettings = { enableSearch: true,
       keyboardControls: true ,idProp : "campaign",
       template: '{{option.campaign.name}}', smartButtonTextConverter(skip, option) { return option; },
       selectionLimit: 4,
       showCheckAll : true,
       scrollableHeight: '300px', scrollable: true};

 $scope.selected_baselines_customTexts = {buttonDefaultText: 'Select Campaigns'};

   $scope.events = {
   onItemSelect : function(item){
       console.log(item);
   }
 }

    $scope.compCampaigns = {
      campaigns : {
        status : 'campaigns', value : false
      }
    };
    $scope.getCompareCampaigns = function(status){
      $scope.compCampaigns.value = false;
      $scope.showPerfMetrics = false;
      $scope.compCampaigns[status].value = !$scope.compCampaigns[status].value;
    }

    $scope.ontimelocation = {
      ontimeloc : {
        status : 'ontimeloc', value : false
      },
      showdrop : {
        status : 'showdrop', value : false
      }
    };
    $scope.getontimelocation = function(status){
      $scope.ontimelocation.value = false;
      $scope.ontimelocation[status].value = !$scope.ontimelocation[status].value;
    }


    $scope.getCompareCampaignChartData = function(campaignChartData){
      console.log(campaignChartData);
      var proposalIdData = [];
      var proposalIdDataNames = {};
      angular.forEach($scope.searchSelectAllModel,function(data){
        proposalIdData.push(data.id.proposal_id);
        proposalIdDataNames[data.id.proposal_id] = {
          name : data.id.name,
        };
        console.log(data);
      })
      DashboardService.getCompareCampaignChartData(proposalIdData)
      .then(function onSuccess(response){
        console.log(response);

        var campaignIds = Object.keys(response.data.data);
        angular.forEach(proposalIdData, function(campaignId){
          if(!(campaignIds.indexOf(campaignId) > -1)){
            response.data.data[campaignId] = {};
            response.data.data[campaignId]['data'] = {};
            response.data.data[campaignId]['total'] = 0;
            response.data.data[campaignId]['interested'] = 0;
            response.data.data[campaignId]['data']['name'] = proposalIdDataNames[campaignId].name;
          }
        });
        formatLineChartData(response.data.data);
        $scope.stackedBarChartOptions = angular.copy(stackedBarChart);
        $scope.stackedBarChartcampaignsData = formatMultiBarChartDataByMultCampaigns(response.data.data);
        $scope.showPerfMetrics = $scope.perfMetrics.multipleLeads;

      }).catch(function onError(response){
        console.log(response);
      })
    }
    var formatMultiBarChartDataByMultCampaigns = function(data){
      var values1 = [];
      var values2 = [];
      angular.forEach(data, function(campaign){
         var value1 =
            { x : campaign.data.name, y : campaign.total - campaign.interested};
         var value2 =
            { x : campaign.data.name, y : campaign.interested};
         values1.push(value1);
         values2.push(value2);
      })
      var temp_data = [
        {
          key : "Normal Leads",
          color : constants.colorKey1,
          values : values1
        },
        {
          key : "High Potential Leads",
          color : constants.colorKey2,
          values : values2
        }
      ];
      console.log(temp_data);
      return temp_data;
    };
    var formatLineChartData = function(data){
      $scope.lineChartLabels = [];
      $scope.lineChartValues = [];
      var values1 = [];
      var values2 = [];

      var count = Object.keys(data).length;
      console.log(data,count);
      angular.forEach(data, function(campaign){
        $scope.lineChartLabels.push(campaign.data.name);
        values1.push(campaign.total/count);
        values2.push((campaign.interested)/count);
      });
      $scope.lineChartValues.push(values1);
      $scope.lineChartValues.push(values2);
      console.log($scope.lineChartLabels,$scope.lineChartValues);
    }
    $scope.lineChartOptions = {
    scales: {
      yAxes: [
        {
          id: 'y-axis-1',
          type: 'linear',
          display: true,
          position: 'left'
        },

      ],
      xAxes: [{
        ticks: {
        autoSkip: false
        }
      }],
      responsive: true,
      maintainAspectRatio: false,
    },
    series: ['Normal','High Potential'],
    legend: {display: true},
    colors: ['#d7525b', '#fcfc5f'],

  };
  $scope.datasetOverride =  [
            {
                fill: true,
                backgroundColor: [
               "#d7525b",

                ]
            },
            {
                fill: true,
                backgroundColor: [
               "#fcfc5f",

                ]
            },
            ];

  $scope.openMenu = function($mdMenu, ev) {
      $mdMenu.open(ev);
    };
    $scope.getSupplierAndInvData = function(data){
      console.log($scope.campaignSupplierAndInvData);
      $scope.supplierAndInvData = $scope.campaignSupplierAndInvData[data.status];
      console.log($scope.supplierAndInvData);

    }

    })//END
  })();
