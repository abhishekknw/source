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
          {header : 'GATEWAY ARCH'},
        ];
        $scope.actKeys = [
          {header : 'RELEASE', key : 'release', label1 : 'Released', label2 : 'UnReleased'},
          {header : 'AUDIT', key : 'audit', label1 : 'Audited', label2 : 'UnAudited'},
          {header : 'CLOSURE', key : 'closure', label1 : 'Closured', label2 : 'UnClosured' },
        ];


        $scope.supHeaders = [
          {header : 'Campaign Name', key : 'proposal_name'},
          {header : 'Inventory', key : 'supplier_name'},
          {header : 'Today Released', key : 'inv_type'},
          {header : 'Average Delay(X)', key : 'act_name'},
          {header : 'Average Off Location(Meters)', key : 'act_name'},
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
            console.log($scope.inventoryActivityCountData);
            angular.forEach(response.data.data, function(data,key){
            $scope.inventoryActivityCountData[key] = sortObject(data);
            console.log($scope.inventoryActivityCountData[key]);
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

        }

        $scope.getPercent = function(num1,num2){
          var percent = num1/num2*100;
          return percent;
        }

        $scope.getAssignedIdsAndImages = function(date,type,inventory){

          console.log(date,type,inventory);
          $scope.invName = inventory;
          $scope.showAssignedInvTable = true;
          DashboardService.getAssignedIdsAndImages(orgId, category, type, date, inventory)
          .then(function onSuccess(response){
            console.log(response);
            $scope.campaignReleaseData = [];
            var campaignReleaseData = [];
            campaignReleaseData['totalOnTimeCount'] = 0;
            campaignReleaseData['totalOfftimeCount'] = 0;
            campaignReleaseData['totalOnLocationCount'] = 0;
            campaignReleaseData['totalOffLocationCount'] = 0;
            campaignReleaseData['totalOffLocationDistance'] = 0;
            campaignReleaseData['totalOffTimeDays'] = 0;
            angular.forEach(response.data.data, function(data,campaignName){
              console.log(data);
              var campaignData = {};
              campaignData['name'] = campaignName;
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

              })
              campaignReleaseData['totalOnTimeCount'] += campaignData['onTimeCount'];
              campaignReleaseData['totalOfftimeCount'] += campaignData['offTimeCount'];
              campaignReleaseData['totalOnLocationCount'] += campaignData['onLocationCount'];
              campaignReleaseData['totalOffLocationCount'] += campaignData['offLocationCount'];
              campaignReleaseData['totalOffLocationDistance'] += campaignData['offLocationDistance'];
              campaignReleaseData['totalOffTimeDays'] += campaignData['offTimeDays'];

              campaignReleaseData.push(campaignData);
            })
            $scope.campaignReleaseData = campaignReleaseData;
            console.log($scope.campaignReleaseData);
            $scope.campaignDataList = [];
            // createList();
            console.log($scope.campaignDataList);
          }).catch(function onError(response){
            console.log(response);
          })
        }

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
              $scope.supplierCodeCountOptions.chart.pie.dispatch['elementClick'] = function(e){ $scope.getCampaignInvTableData(e.data); };

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
         getCampaignInventoryActivitydetails(campaignId);
         $scope.getCampaignFilters(campaignId);
         DashboardService.getSuppliersOfCampaignWithStatus(campaignId)
         .then(function onSuccess(response){
           $scope.showLeadsDetails = true;
           console.log(response);
           $scope.campaignStatusData = response.data.data;
           console.log($scope.campaignStatusData);
           $scope.showSupplierSocietywiseInvTable = false;
           $scope.showSupplierInvdDataTable = function(invData){
             $scope.SocietyInvTable = $scope.campaignStatusData;
             console.log($scope.campaignStatusData.ongoing);
             // $scope.SocietyInvTable = [
             //   { SocietyTitle : $scope.campaignStatus.ongoing.campaignLabel},
             //   { SocietyTitle : $scope.campaignStatus.completed.campaignLabel},
             //   { SocietyTitle : $scope.campaignStatus.upcoming.campaignLabel}
             // ];
             console.log($scope.SocietyInvTable.ongoing.supplier);
             $scope.showSupplierSocietywiseInvTable = true;
           };
           $scope.countallsupplier = $scope.campaignStatusData.completed.length+$scope.campaignStatusData.ongoing.length+$scope.campaignStatusData.upcoming.length;
           // console.log($scope.countallsupplier);
           var totalFlats=0,totalLeads=0,totalSuppliers=0,hotLeads=0;
           // $scope.totalLeadsCount = response.data.data.supplier_data.length;
           angular.forEach($scope.campaignStatusData, function(data,key){
              if($scope.campaignStatusData[key].length){
                $scope.campaignStatusData[key]['totalFlats'] = 0;
                $scope.campaignStatusData[key]['totalLeads'] = 0;
                $scope.campaignStatusData['totalSuppliers'] = 0;
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

       $scope.getCampaignInvTableData = function(campaigns){
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
        // console.log($scope.campaignInventoryTypesData.supplier_data);
        $scope.getSupplierInvTableData($scope.campaignInventoryTypesData);
        $scope.campaignInventoryData = response.data.data;
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
        // console.log($scope.campaignInventoryActivityData);
        }).catch(function onError(response){
      console.log(response);
    })
   }


    })//END
  })();
