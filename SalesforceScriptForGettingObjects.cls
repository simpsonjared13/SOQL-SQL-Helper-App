salesforcescript String objectName = 'ObjectAPIName'; //You must change the object API name in the following line to get info!!! 
Map<String, Schema.SObjectField> fieldMap = Schema.SObjectType.ObjectAPIName.fields.getMap(); 
//Schema.SObjectField test = fieldMap.get('Client_Segment__c'); 
//System.debug(test.getDescribe()); 
String message ='';
// + test.getDescribe(); 
for(Schema.SObjectField sof : fieldMap.values()){ 
    Schema.DescribeFieldResult dfr = sof.getDescribe(); 
    message+= 'Name:'+ dfr.getName() + ', Type:' + dfr.getType() + ', Length:' + dfr.getLength() + ', 
        Precision:' + dfr.getPrecision() + ', Default Value:' + dfr.getDefaultValue() + + ', 
        Scale:' + dfr.getScale() + ', Digits:' + dfr.getDigits() + + ', Unique:' + dfr.isUnique() + ', 
        AutoNumber:' + dfr.isAutoNumber() + ', Label:' + dfr.getLabel() + ', Formula:' + dfr.isCalculated(); message+='\n'; 
} 
//System.debug(message); 
Messaging.reserveSingleEmailCapacity(1); 
Messaging.SingleEmailMessage mail = new Messaging.SingleEmailMessage();
String[] toAddresses = new String[] {'example@email.com'};
mail.setToAddresses(toAddresses); 
mail.setSubject('' + objectName + ' Details'); 
mail.setPlainTextBody(message); 
Messaging.sendEmail(new Messaging.SingleEmailMessage[] { mail });
