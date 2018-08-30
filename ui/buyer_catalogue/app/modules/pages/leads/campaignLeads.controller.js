"use strict";
angular.module('catalogueApp')
    .controller('CampaignLeadsCtrl', function($scope, $rootScope, $stateParams, $window, $location, campaignLeadsService ,$http, constants, permissions, commonDataShare) {
      $scope.modelData = {};
      $scope.modelData['alias_data'] = [];
      $scope.savedFormFields = [];
      $scope.importLeadsData = [];
      $scope.showImportTable = false;
      $scope.formName = {
        name : undefined
      }
      var formatedLeadsList = [];
      $scope.leadFormFields = [];
      $scope.optionForm = {
        option : undefined
      };
      console.log("hello");
      $scope.optionsDummy = [
        {name : 'STRING'},
        {name : 'INT'},
        {name : 'EMAIL'},
        {name : 'PASSWORD'},
        {name : 'PHONE'},
        {name : 'RADIO'},
        {name : 'DROPDOWN'},
        {name : 'CHECKBOX'},
        {name : 'TEXTAREA'},
      ];
      $scope.leadKeyTypes = [
        {name : 'STRING'},
        {name : 'INT'},
        {name : 'EMAIL'},
        {name : 'PASSWORD'},
        {name : 'PHONE'},
        {name : 'RADIO'},
        {name : 'DROPDOWN'},
        {name : 'CHECKBOX'},
        {name : 'TEXTAREA'},
      ];
      $scope.keyTypesMap = {
        'STRING' : 'text',
        'INT' : 'number',
        'EMAIL' : 'email',
        'PASSWORD' : 'password',
        'PHONE' : 'number',
        'RADIO' : 'radio',
        'CHECKBOX' : 'checkbox',
        'TEXTAREA' : 'textarea'
      }
      var leadFormField = {
        key_name : '',
        key_type : '',
        order_id : 1
      };
      $scope.campaignHeaders = [
        {header : 'Campaign Name'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Action'},
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
        {name : 'alphanumeric3', value : false},
        {name : 'alphanumeric4', value : false},
        {name : 'boolean1', value : false},
        {name : 'boolean2', value : false},
        {name : 'boolean3', value : false},
        {name : 'boolean4', value : false},
        {name : 'float1', value : false},
        {name : 'float2', value : false},
        {name : 'number1', value : false},
        {name : 'number2', value : false},
        {name : 'date1', value : false},
        {name : 'date2', value : false},
        {name : 'is_interested', value : false},
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
      $scope.saveLeadForm = function(){
        var data = {
          leads_form_name : $scope.formName.name,
          leads_form_items : $scope.leadFormFields
        }
        console.log(data);
        angular.forEach(data.leads_form_items, function(item,index){
          item.order_id = index + 1;
        })
        campaignLeadsService.createLeadForm(data,$scope.campaignId)
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
      $scope.getEntryListLeads = function(){
             campaignLeadsService.getEntryListLeads($scope.leadFormId,$scope.supplierData.supplier_id)
             .then(function onSuccess(response){
               console.log(response);
               $scope.showLeads = true;
               $scope.entryListLeadsData = response.data.data;
               console.log($scope.entryListLeadsData.values);
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
      $scope.removeField = function(index){
        $scope.leadFormFields.splice(index,1);
      }
      var assigned_by = '0';
      var fetch_all = '0';
      var userId = $rootScope.globals.currentUser.user_id;
      $scope.Data = [];
      campaignLeadsService.getCampaignDetails(assigned_by,userId,fetch_all)
        .then(function onSuccess(response){
          console.log(response);
          $scope.campaigns = response.data.data;
          $scope.Data = $scope.campaigns;
          console.log($scope.Data);
          $scope.loading = response.data.data;

        })
        .catch(function onError(response){
          console.log(response);
        });
      $scope.addField();
      $scope.changeView = function(view,campaign,formFields){
        $scope.views = {
          createForm : false,
          viewLeads : false,
          campaigns : false,
          addLeads : false,
          enterLeads : false,
          selectSuppliers : false,
          importLeads : false,
          viewLeadForms : false
        }
        $scope.views[view] = true;
        $scope.campaignInfo = campaign;
        if(formFields)
        {
          $scope.leadFormFields = formFields;
        }

        console.log(view,campaign);
        switch(true){
          case $scope.views.viewLeadForms:
            $scope.campaignId = campaign.campaign.proposal_id;
            $scope.savedFormFields = [];
            getCampaignLeadForms($scope.campaignId);
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
          case $scope.views.createForm:
            break;
          case $scope.views.enterLeads:
            break;
        }
      }
      var getCampaignLeadForms = function(campaignId){
        campaignLeadsService.getCampaignLeadForms(campaignId)
        .then(function onSuccess(response){
          console.log(response);
          $scope.leadForms = response.data.data;
          console.log($scope.leadFormFields, $scope.formName.name);
          // getLeads(campaignId);
          // $scope.modelData.alias_data = response.data.data;
          // checkSavedFields();
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

      $scope.getLeadForm = function(item){
        $scope.formName.name = undefined;
        $scope.leadFormFields = [];

        if(item){
          $scope.formName.name = item.leads_form_name;
          $scope.leadFormFields = item.leads_form_items;
        }
        else{
          console.log($scope.leadFormFields,leadFormField);
          $scope.leadFormFields.push(angular.copy(leadFormField));
        }
        $scope.changeView('createForm');
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
            createBulkLeadsList($scope.importLeadsData,$scope.aliasData,headerNames);
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
      var createBulkLeadsList = function(importLeadsData, aliasData, headers){
        formatedLeadsList = [];
        console.log(headers);
        for(var i=0; i<importLeadsData.length; i++){
          var data = {};
          if(!(headers.indexOf('SUPPLIER_ID') > -1)){
            alert('There is No SUPPLIER_ID Column, Please Add and ReInsert the Sheet');
            $scope.resetData();
            break;
          }
          data['campaign_id'] = $scope.campaignId;
          data['object_id'] = importLeadsData[i].SUPPLIER_ID;
          for(var j=0; j<aliasData.length; j++){
            data[aliasData[j].original_name] = importLeadsData[i][aliasData[j].alias];
          }
          formatedLeadsList.push(data);
        }
        console.log(formatedLeadsList);
      }
      // END : create list of leads to bulk insert

      // START: call to create leads API through sheet
      $scope.importLeadsThroughSheet = function(){
        var token = $rootScope.globals.currentUser.token;
        if ($scope.file) {
          Upload.upload({
              url: constants.base_url + constants.url_base + "leads/" + $scope.formId + "/import_leads",
              data: {
                file: $scope.file,
                data_import_type : "base-data"
              },
              headers: {'Authorization': 'JWT ' + token}
          }).then(function onSuccess(response){
                console.log(response);

          })
          .catch(function onError(response) {
              console.log(response);

            });
      }
      }
      // END:   call to create leads API through sheet
      // START: add lead form fields

      $scope.leadFormFields.push(angular.copy(leadFormField));

      $scope.addLeadFormFields = function(){
        console.log($scope.leadFormFields);
        $scope.leadFormFields.push(angular.copy(leadFormField));
      }


      // END: add lead form fields
      $scope.addKeyOption = function(option,index){

        if(!$scope.leadFormFields[index].hasOwnProperty('key_options')){
            $scope.leadFormFields[index]['key_options'] = [];
        }
        $scope.leadFormFields[index]['key_options'].push(option);
        $scope.optionForm.option = undefined;
        }


      $scope.getMultipleLeadForms = function(supplier){
        $scope.changeView('viewLeadForms',$scope.campaignInfo);
      }
      $scope.enterLeads = function(supplier){
        console.log($scope.leadFormFields);
        $scope.leadModelData = [];
        $scope.leadModelData = angular.copy($scope.leadFormFields.leads_form_items);
        $scope.leadFormId = $scope.leadFormFields.leads_form_id;
        $scope.changeView('enterLeads',$scope.campaignInfo,$scope.leadFormFields);
        $scope.supplierData = supplier;

        console.log(supplier);
      }
      $scope.saveLeads = function(){
        var data = {
          supplier_id : $scope.supplierData.supplier_id,
          leads_form_entries : []
        };
        angular.forEach($scope.leadModelData, function(item){
            var temp_data = {
              item_id : item.item_id,
              value : item.value
            }
            data.leads_form_entries.push(temp_data);
        });
        console.log(data);
        campaignLeadsService.saveLeads($scope.leadFormId,data)
        .then(function onSuccess(response){
          console.log(response);
        }).catch(function onError(response){
          console.log(response);
        })

      }


      $scope.updateSelection = function(position, option) {
        angular.forEach(option, function(item, index) {
          if (position != index)
            item.value = false;
        });
      }
      $scope.setCheckBoxValue = function(isSelected,index,values){
        console.log(values);
        if(!values.hasOwnProperty('value')){
          values['value'] = [];
        }
        console.log(isSelected);
        if(isSelected){
          values.value.push($scope.leadChBoxKeyOptions[index].name);
        }else {
          console.log("hello");
          values.value.splice(values.value.indexOf($scope.leadChBoxKeyOptions[index].name),1);
        }
        console.log(values,$scope.leadModelData);
      }
      $scope.getCheckBoxValues = function(values){
        console.log(values);
        $scope.leadChBoxKeyOptions = [];
        angular.forEach(values, function(value,index){
          $scope.leadChBoxKeyOptions[index] = {
            name : value, selected : false
          };
        });
        console.log($scope.leadChBoxKeyOptions);
      }
      $scope.uploadFiles = function(file){
        $scope.file = file;
      }

    });//Controller ends here
