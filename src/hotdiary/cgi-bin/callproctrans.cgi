#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: callproctrans.cgi
# Purpose: call process transactions
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;

# Read in all the variables set by the form
   &ReadParse(*input);


   ## URL Manager section of the settings menu. x_ADC_URL field.
   ## 1. x_response_code (1 = Approved, 2 = Declined, 3=Error)
   ## 2. x_response_subcode = A code used by the system for internal
   ##    transaction tracking
   ## 3. x_response_reason_code = A Code giving more details about the the 
   ## transaction
   ## 4. x_response_reason_text = Brief description of result, which corresponds
   ##                  with the Response Reason Code 
   ## 5. x_auth_code = 6 digit approval code
   ## 6. x_avs_code = Indicates the result of Address Verification System (AVS)
   ##  checks.
   ##                        A = Address (Street) matches, ZIP does
   ##                        not
   ##                        E = AVS error
   ##                        N = No Match on Address (Street) or ZIP
   ##                        P = AVS not applicable for this
   ##                        transaction
   ##                        R = Retry - System unavailable or timed
   ##                        out
   ##                        S = Service not supported by issuer
   ##                        U = Address information is unavailable
   ##                        W = 9 digit ZIP matches, Address
   ##                        (Street) does not
   ##                        X = Exact AVS Match
   ##                        Y = Address (Street) and 5 digit ZIP
   ##                        match
   ##                        Z = 5 digit ZIP matches, Address
   ##                        (Street) does not
   ## 7. x_trans_id = This number identifies the transaction
   ##                        in the system, and can be used to submit
   ##                        a modification of this transaction at a
   ##                        later time via HTML form POST (such as
   ##                        voiding the transaction, or capturing an Auth only
   ##    transaction

   ## list of the input values are echoed
   ## 8.x_invoice_num, 9. x_description,  10. x_amount, 11. x_method
   ## 12. x_type, 13. x_cust_id, 14. x_first_name, 15. x_last_name,
   ## 16. x_company, 17. x_address, 18. x_city, 19. x_state, 20. x_zip
   ## 21. x_country, 22. x_phone, 23. x_fax, 24. x_email, 25. x_ship_to_first_name
   ## 26. x_ship_to_last_name, 27. x_ship_to_company, 28. x_ship_to_address
   ## 29. x_ship_to_city, 30. x_ship_to_state, 31. x_ship_to_zip,
   ## 32. x_ship_to_country, 33. x_tax,  34. x_duty, 35. x_freight, 36. x_tax_exempt

   ## 37. x_po_num, 38. x_md5_hash, 39. any other our fields defined. 

   ## x_md5_hash = generated by the system and to be validated by merchant 
   ##     for added security


   ## https://secure.authorize.net/gateway/transact.dll 
   ## x_ADC_Relay_Response - This field must be in the form and set to a value 
   ## 
   ## of TRUE to tell the system that it will be doing an ADC Relay Response 
   ## transaction. 

   ## x_ADC_URL - The value of this field is the URL to which the system will 
   ## return the results of the transaction. The results of the transaction 
   ## will be returned via a HTTP form POST to the specified URL. As an extra 
   ## security 
   ## precaution, the URL specified in this field must be a Valid ADC or Receipt 
   ##  Link URL, as specified in the URL Manager. 

   ## values that are defaulted are:
   ## x_Bank_Acct_Type=CHECKING (if this is not passed.
   ## x_Color_Background=#FFFFFF (white)
   ## x_Color_Link=Blue or #0000FF
   ## x_Color_Text= Black or #000000
   ## x_Email_Customer=TRUE
   ## x_Email_Merchant=TRUE
   ## x_Receipt_Link_Method=LINK
   ## x_Receipt_Link_Text=Continue (any string can be specified)
   ## x_Tax_Exempt=False


  