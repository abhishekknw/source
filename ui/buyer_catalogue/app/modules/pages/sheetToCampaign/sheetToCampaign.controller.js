angular.module('catalogueApp')

.controller('sheetToCampaignController', ['$scope', '$rootScope', '$window',
              '$location','commonDataShare','constants','campaignListService',
              'pagesService','createProposalService','sheetToCampaignService',
    function ($scope, $rootScope, $window, $location , commonDataShare,constants,
                campaignListService, pagesService,createProposalService,sheetToCampaignService) {
      console.log($rootScope);
      $scope.invoiceNumber = {
        id : null
      }
      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;
      $scope.popup3 = false;
      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      // $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.formats = ['yyyy-MM-dd'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];

      $scope.dateData = {};
      $scope.spaces = [
    		{name:"Societies", code:"RS", selected:"false"},
    		{name:"Corporate Parks", code:"CP", selected:"false"},
    		{name:"Bus Shelter", code:"BS", selected:"false"},
    		{name:"Gym", code:"GY", selected:"false"},
    		{name:"Saloon", code:"SA", selected:"false"},
    		{name:"Retail Shop", code:"RE", selected:"false"},
    	];
      $scope.filters = [
        {name : 'Poster(PO)',  code : 'PO',   selected : false },
        {name : 'Standee(ST)', code : 'ST',   selected : false },
        {name : 'Stall(SL)',   code : 'SL',   selected : false },
        {name : 'Flyer(FL)',   code : 'FL',   selected : false },
      ]
      $scope.model = {
        centers : [
          {
            center : {
                codes : [],
          },
        },
        ],
      };
      console.log($scope.model);
      $scope.societyData = {};
      $scope.cityKey = {};
      $scope.areaKey = {};
      $scope.areas = [];
      $scope.searchSelectAllSettings = { enableSearch: true,
          keyboardControls: true ,idProp : 'supplier_id',
          template: '{{option.name}}, {{option.area}}', smartButtonTextConverter(skip, option) { return option; },
          scrollableHeight: '300px', scrollable: true};
      $scope.filterSettings = { enableSearch: true,
          keyboardControls: true ,idProp : 'code',
          template: '{{option.name}}', smartButtonTextConverter(skip, option) { return option; },
          scrollableHeight: '300px', scrollable: true};
      $scope.events = {
        onItemSelect : function(item){
            item['status'] = 'F';
            console.log(item);
        }
      }
      $scope.searchSelectAllModel = [];
      $scope.searchSelectAllData = [];
      $scope.filterModel = [];
      $scope.example5customTexts = {buttonDefaultText: 'Select Suppliers'};
      $scope.filterTexts = {buttonDefaultText: 'Select Filters'};
      var orgId = $rootScope.globals.userInfo.profile.organisation.organisation_id;
      console.log(orgId);
      var getOrganisations = function(){
        pagesService.getOrganisations(orgId)
        .then(function onSuccess(response){
          $scope.orgnisations = response.data.data;
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }
      var getCities = function(){
      createProposalService.loadInitialData()
        .then(function onSuccess(response){
          console.log(response);
            $scope.cities = response.data.cities;
    				angular.forEach($scope.cities, function(data){
              $scope.cityKey[data.city_name] = data;
            })
            console.log($scope.cityKey);
          }).catch(function onError(response){
    				commonDataShare.showErrorMessage(response);
    				console.log("Error occured");
    			});
        }
        var init = function(){
          getCities();
          getOrganisations();
        }

        init();
      $scope.getAccounts = function(orgId){
        pagesService.getAccounts(orgId)
        .then(function onSuccess(response){
          $scope.accounts = response.data.data;
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }

      $scope.createProposal = function(){
        console.log($scope.model);
        $scope.proposalCreated = true;
        if($scope.model.centers[0].center.pincode)
          $scope.model.centers[0].center.pincode = $scope.model.centers[0].center.pincode.toString();
        createProposalService.saveInitialProposal($scope.model.account_id, $scope.model)
        .then(function onSuccess(response){
          console.log(response);
          $scope.proposalId = response.data.data;
          getSocieties();
          getProposalCenters();

        }).catch(function onError(response){
          console.log(response);
        })

      }
      $scope.getArea = function(city){
        console.log(city);
        createProposalService.getLocations('areas', city)
           .then(function onSuccess(response){
             $scope.areas = response.data;
             console.log($scope.areaList);
             angular.forEach($scope.areas, function(data){
               $scope.areaKey[data.label] = data;
             })
             console.log($scope.areaKey);
             }).catch(function onError(response){
     					commonDataShare.showErrorMessage(response);
             });
        }
        $scope.getSubArea = function(area){
          console.log(area);
          createProposalService.getLocations('sub_areas', area)
             .then(function onSuccess(response){
                 $scope.subAreas = response.data;
                 console.log(response);
               });
        }
        $scope.checkSpace = function(supplier,center){
          console.log(center);
      		if(supplier.selected == true)
      			center.center.codes.push(supplier.code);
      		else {
      			var index = center.center.codes.indexOf(supplier.code);
      			if(index > -1)
      				center.center.codes.splice(index,1);
      		}
      	}
        var getSocieties = function(){
          sheetToCampaignService.getSocieties()
          .then(function onSuccess(response){
            console.log(response);
            $scope.searchSelectAllData = response.data.data.societies;
            angular.forEach($scope.searchSelectAllData, function(data){
              $scope.societyData[data.supplier_id] = data;
            })
          }).catch(function onError(response){
            console.log(response);
          })
        }
        var getProposalCenters = function(){
          sheetToCampaignService.getProposalCenters($scope.proposalId)
          .then(function onSuccess(response){
            $scope.centerData = response.data.data[0];
            console.log(response);
          }).catch(function onError(response){
            console.log(response);
          })
        }

        $scope.submit = function(){
          var filterAndSupplierData = getFilterAndSupplierData();
          filterAndSupplierData['proposal_id'] = $scope.proposalId;
          filterAndSupplierData['center_id'] = $scope.centerData.id;
          filterAndSupplierData['invoice_number'] = $scope.invoiceNumber.id;
          filterAndSupplierData['tentative_start_date'] = $scope.dateData.tentative_start_date;
          filterAndSupplierData['tentative_end_date'] = $scope.dateData.tentative_end_date;
          console.log(filterAndSupplierData);
          sheetToCampaignService.convertDirectProposalToCampaign(filterAndSupplierData)
          .then(function onSuccess(response){
            console.log(response);
            swal(constants.name,constants.proposal_to_campaign,constants.success);
          }).catch(function onError(response){
            console.log(response);
          })
        }
        var getFilterAndSupplierData = function(){
          var data = {};
            data['center_data'] = {
              RS : {
                filter_codes : $scope.filterModel,
                supplier_data : $scope.searchSelectAllModel,
              }
            }
          return data;
        }
}]);
