"use strict";
angular.module('catalogueApp')
    .controller('CampaignLeadsCtrl', function($scope, $rootScope, $stateParams, $window, $location, campaignLeadsService ,$http, constants, permissions, commonDataShare) {
      $scope.modelData = {};
      $scope.modelData['alias_data'] = [];
      $scope.savedFormFields = [];
      $scope.importLeadsData = [];
      $scope.showImportTable = false;
      var formatedLeadsList = [];
      console.log("hello");
      $scope.campaignHeaders = [
        {header : 'Campaign Name'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Action'},
        {header : 'Action'},
        {header : 'Action'},
      ];
      var formFieldsStruct = [
        {name : 'firstname1' , value : false},
        {name : 'lastname1' , value : false},
        {name : 'firstname2' , value : false},
        {name : 'lastname2' , value : false},
        {name : 'mobile1' , value : false},
        {name : 'mobile2' , value : false},
        {name : 'phone' , value : false},
        {name : 'email1' , value : false},
        {name : 'email2' , value : false},
        {name : 'address' , value : false},
        {name : 'alphanumeric1', value : false},
        {name : 'alphanumeric2', value : false},
        {name : 'boolean1', value : false},
        {name : 'boolean2', value : false},
      ];
      $scope.formFields = angular.copy(formFieldsStruct);
      $scope.views = {
        viewLeads : false,
        createForm : false,
        campaigns : true,
        addLeads : false,
        enterLeads : false,
        selectSuppliers : false,
      }
      $scope.create = function(){
        $scope.modelData['campaign'] = $scope.campaignId;
        console.log($scope.modelData);
        campaignLeadsService.create($scope.modelData)
        .then(function onSuccess(response){
          console.log(response);
          swal(constants.name,constants.create_success,constants.success);
        }).catch(function onError(response){
          console.log(response);
        })
      }
      //checkSavedFields function is used to disable selected fields in dropdown ui of formFields
      var checkSavedFields = function(){
        angular.forEach($scope.modelData.alias_data, function(field){
          $scope.savedFormFields[field.original_name] = field;
        })
      }
      var getLeads = function(campaignId){
        campaignLeadsService.getLeads(campaignId)
        .then(function onSuccess(response){
          console.log(response);
          $scope.leadsData = response.data.data;
        }).catch(function onError(response){
          console.log(response);
        })
      }

      $scope.addField = function(){
        var data = {
          alias : '',
          original_name : ''
        }
        $scope.modelData.alias_data.push(data);
        checkSavedFields();
      }
      var assigned_by = '0';
      var fetch_all = '0';
      var userId = $rootScope.globals.currentUser.user_id;
      campaignLeadsService.getCampaignDetails(assigned_by,userId,fetch_all)
        .then(function onSuccess(response){
          console.log(response);
          $scope.campaigns = response.data.data;
        })
        .catch(function onError(response){
          console.log(response);
        });
      $scope.addField();
      $scope.changeView = function(view,campaign){
        $scope.views = {
          createForm : false,
          viewLeads : false,
          campaigns : false,
          addLeads : false,
          enterLeads : false,
          selectSuppliers : false,
          importLeads : false
        }
        $scope.views[view] = true;
        console.log(view,$scope.views.createForm);
        switch(true){
          case $scope.views.createForm:
            $scope.campaignId = campaign.campaign.proposal_id;
            getCampaignLeadAliasData($scope.campaignId);
            console.log($scope.campaignId);
            break;
          case $scope.views.selectSuppliers:
            $scope.campaignId = campaign.campaign.proposal_id;
            getShortlistedSuppliers($scope.campaignId);
            $scope.campaignName = campaign.campaign.name;
            break;
          case $scope.views.viewLeads:
            $scope.campaignId = campaign.campaign.proposal_id;
            $scope.campaignName = campaign.campaign.name;
            getLeads($scope.campaignId);
            break;
          case $scope.views.importLeads:
            $scope.campaignId = campaign.campaign.proposal_id;
            $scope.campaignName = campaign.campaign.name;
            $scope.aliasData = [];
            getAliasData($scope.campaignId);
            $scope.importLeadsData = [];
            $scope.showImportTable = false;
            break;
        }
      }
      var getCampaignLeadAliasData = function(campaignId){
        campaignLeadsService.getCampaignLeadAliasData(campaignId)
        .then(function onSuccess(response){
          console.log(response,$scope.modelData);
          $scope.modelData.alias_data = response.data.data;
          checkSavedFields();
        }).catch(function onError(response){
          console.log(response);
        })
      }

      var getShortlistedSuppliers = function(campaignId){
        campaignLeadsService.getShortlistedSuppliers(campaignId)
        .then(function onSuccess(response){
          $scope.suppliers = [];
          $scope.shortlisted_suppliers = response.data.data;
          for(var centerId in $scope.shortlisted_suppliers){
            for(var supplierType in $scope.shortlisted_suppliers[centerId].suppliers){
              angular.forEach($scope.shortlisted_suppliers[centerId].suppliers[supplierType], function(supplier){
                supplier['supplierCode'] = supplierType;
              })
              angular.extend($scope.suppliers,$scope.shortlisted_suppliers[centerId].suppliers[supplierType]);
            }
          }
          console.log($scope.suppliers);
        }).catch(function onError(response){
          console.log(response);
        })
      }

      $scope.getLeadForm = function(supplier){
        $location.path('/leadsForm/' + supplier.supplierCode + '/' + $scope.campaignId + '/' + supplier.supplier_id);
      }
      // start : to read excel sheet while importing lead sheet
      $scope.read = function(workbook){
        console.log(workbook);
        var headerNames = XLSX.utils.sheet_to_json( workbook.Sheets[workbook.SheetNames[0]], { header: 1 })[0];
				var data = XLSX.utils.sheet_to_json( workbook.Sheets[workbook.SheetNames[0]]);
        $scope.importLeadsData = data;
        if($scope.importLeadsData.length && $scope.aliasData){
          $scope.$apply(function(){
            $scope.showImportTable = true;
            checkHeaders(headerNames);
            createBulkLeadsList($scope.importLeadsData,$scope.aliasData);
           });

          console.log("hello");
        }
        console.log($scope.importLeadsData);
      }
      var getAliasData = function(campaign){
        campaignLeadsService.getAliasData(campaign)
        .then(function onSuccess(response){
          $scope.aliasData = response.data.data;
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })
      }

      // START : check sheet headers with aliasData headers
      var checkHeaders = function(headersList){
        var error = false;
        var headers = [];
        angular.forEach($scope.aliasData, function(alias,index){
          if(!(alias.alias == headersList[index])){
            console.log(headers);
            alert("error in header field " + alias.alias + 'and' + headersList[index]);
            error = true;
          }
          headers.push(alias.alias);
          console.log(alias,index);
        })
        if(error){
          alert("Header Sequence should be :" + headers);
        }
      }
      // END : check sheet headers with aliasData headers

      //START : to reset sheet data
      $scope.resetData = function(){
        $scope.importLeadsData = [];
        $scope.showImportTable = false;
      }
      //END : to reset sheet data

      // START : create list of leads to bulk insert
      var createBulkLeadsList = function(importLeadsData, aliasData){
        formatedLeadsList = [];
        for(var i=0; i<importLeadsData.length; i++){
          var data = {};
          if(!(importLeadsData[i].hasOwnProperty('SUPPLIER_ID'))){
            alert('There is No SUPPLIER_ID Column, Please Add and ReInsert the Sheet');
            $scope.resetData(); 
            break;
          }

          data['supplier_id'] = importLeadsData[j].SUPPLIER_ID;
          for(var j=0; j<aliasData.length; j++){
            data[aliasData[j].original_name] = importLeadsData[i][aliasData[j].alias];
          }
          formatedLeadsList.push(data);
        }
        console.log(formatedLeadsList);
      }
      // END : create list of leads to bulk insert

    });//Controller ends here
