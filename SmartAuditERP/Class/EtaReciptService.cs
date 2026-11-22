using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using AuditorAPI.Models;
using AuditorAPI.Models.DGVmodels;
using ETA_Invoice;
using ETA_Invoice.Models;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using QRCoder;

namespace SmartAuditERP
{

        public class EtaReciptService
        {
                public async Task<bool> sendERecitp(Invoice invoice)
                {
                        Customer customer;
                        customer = new Customer(invoice.Customer);
                        double num;
                        num = 0.0;
                        double num2;
                        num2 = 0.0;
                        // P6-018 fix: مجاميع عشرية من قيم البنود نفسها — الرأس يُبنى منها
                        // فيطابق بنوده حرفيًا (كان الرأس يُسند من حقول الفاتورة بمقاييس
                        // مختلفة فلا يتطابق netAmount/totalSales/الخصم مع البنود).
                        decimal salesTotalSum;
                        salesTotalSum = 0m;
                        decimal netSaleSum;
                        netSaleSum = 0m;
                        decimal lineTotalSum;
                        lineTotalSum = 0m;
                        decimal vatSum;
                        vatSum = 0m;
                        decimal withholdingSum;
                        withholdingSum = 0m;
                        decimal itemsDiscountSum;
                        itemsDiscountSum = 0m;
                        List<pos_liens> list;
                        list = new List<pos_liens>();
                        foreach (InvoiceItem invoiceItem in invoice.InvoiceItems)
                        {
                                // P6-018 fix: قيم البند مرة واحدة ثم تُستعمل للبند والمجموع
                                decimal lineTotalSale;
                                lineTotalSale = new decimal(invoiceItem.ItemPriceWithoutVAT * invoiceItem.ItemQuantity);
                                decimal lineDiscount;
                                lineDiscount = new decimal(invoiceItem.ItemDiscount);
                                decimal lineNetSale;
                                lineNetSale = decimal.Subtract(lineTotalSale, lineDiscount);
                                decimal lineVat;
                                lineVat = new decimal(invoiceItem.ItemVat);
                                decimal lineWithholding;
                                lineWithholding = new decimal(Math.Round((invoiceItem.ItemTotalPrice - invoiceItem.ItemDiscount) * invoiceItem.WithholdingTaxPerc / 100.0, 5));
                                decimal lineTotal;
                                lineTotal = decimal.Subtract(decimal.Add(lineNetSale, lineVat), lineWithholding);
                                pos_liens pos_liens;
                                pos_liens = new pos_liens
                                {
                                        description = invoiceItem.ItemName,
                                        itemType = invoiceItem.EgyCodeType,
                                        itemCode = invoiceItem.EgyItemCode,
                                        unitType = invoiceItem.UnitCode,
                                        unitPrice = new decimal(invoiceItem.ItemPriceWithoutVAT),
                                        quantity = new decimal(invoiceItem.ItemQuantity),
                                        internalCode = invoiceItem.ItemCode,
                                        totalSale = lineTotalSale,
                                        total = lineTotal,
                                        valueDifference = 0m,
                                        netSale = lineNetSale
                                };
                                pos_liens.discountlist = new List<commercialDiscountData>();
                                pos_liens.discountlist.Add(new commercialDiscountData
                                {
                                        amount = lineDiscount,
                                        description = "Discount"
                                });
                                pos_liens.taxelists = new List<invoice_line_taxelist>();
                                pos_liens.taxelists.Add(new invoice_line_taxelist
                                {
                                        taxType = "T1",
                                        amount = lineVat,
                                        rate = new decimal(invoiceItem.ItemVatPerc),
                                        subType = "V009"
                                });
                                num += Math.Round((invoiceItem.ItemTotalPrice - invoiceItem.ItemDiscount) * invoiceItem.WithholdingTaxPerc / 100.0, 5);
                                num2 += invoiceItem.ItemDiscount;
                                salesTotalSum = decimal.Add(salesTotalSum, lineTotalSale);
                                netSaleSum = decimal.Add(netSaleSum, lineNetSale);
                                lineTotalSum = decimal.Add(lineTotalSum, lineTotal);
                                vatSum = decimal.Add(vatSum, lineVat);
                                withholdingSum = decimal.Add(withholdingSum, lineWithholding);
                                itemsDiscountSum = decimal.Add(itemsDiscountSum, lineDiscount);
                                list.Add(pos_liens);
                        }
                        if (Operators.CompareString(EtaSetting.DocumentTypeVersion, "V1.0", TextCompare: false) == 0)
                        {
                        }
                        try
                        {
                                if (Operators.CompareString(EtaSetting.EinvoieType, "production", TextCompare: false) == 0)
                                {
                                        config_class.BaseUrl = "https://api.invoicing.eta.gov.eg";
                                        config_class.tok_url = "https://id.eta.gov.eg/connect/token";
                                }
                                else
                                {
                                        // P6-019 fix: مضيف API الموثق لغير الإنتاج — كان BaseUrl
                                        // يشير إلى مضيف الهوية (id.preprod) فيذهب طلب الإرسال
                                        // إلى خدمة التوكن بدل خدمة المستندات.
                                        config_class.BaseUrl = "https://api.preprod.eta.gov.eg";
                                        config_class.tok_url = "https://id.preprod.eta.gov.eg/connect/token";
                                }
                                config_class.client_id = EtaSetting.EtaClientId;
                                config_class.client_secret = EtaSetting.EtaClientSecret1;
                                config_class.os = "windows";
                                config_class.pos_eta_serial = EtaSetting.PosEtaSerial;
                                new send_respons_model();
                                pos_document pos_document;
                                pos_document = new pos_document();
                                buyer buyer;
                                buyer = new buyer();
                                pos_seller pos_seller;
                                pos_seller = new pos_seller();
                                pos_document.receiptNumber = Conversions.ToString(invoice.InvoiceNo);
                                pos_document.grossWeight = 0m;
                                pos_document.exchangeRate = 0m;
                                pos_document.netWeight = 0m;
                                pos_document.receiptType = "s";
                                pos_document.typeVersion = "1.2";
                                if (invoice.ProcType == 2)
                                {
                                        pos_document.receiptType = "r";
                                        pos_document.typeVersion = "1.2";
                                }
                                pos_document.uuid = "";
                                // P6-015 fix: وقت الإصدار كامل (كان التاريخ فقط — الوقت
                                // يسقط) وتحويل UTC حقيقي (كان يُلصق Z على توقيت محلي).
                                pos_document.dateTimeIssued = invoice.InvDate.ToUniversalTime();
                                pos_document.previousUUID = invoice.previousUUID;
                                if (invoice.ProcType == 2)
                                {
                                        pos_document.referenceUUID = InvoiceOper.GetInvoiceUUID(invoice.ReffNo, 3, 1, invoice.Branch);
                                }
                                pos_document.referenceOldUUID = "";
                                pos_document.currency = "EGP";
                                pos_document.exchangeRate = 1m;
                                // P6-018 fix: الرأس يُبنى من مجاميع البنود نفسها فيتطابق معها:
                                // totalSales = Σ totalSale للبنود؛ totalCommercialDiscount =
                                // Σ خصوم البنود + خصم مستوى الفاتورة؛ netAmount = Σ netSale
                                // (بعد الخصوم، قبل الضرايب)؛ totalAmount = Σ total البنود
                                // (netSale + T1 − الاستقطاع) — كان الرأس يُسند من
                                // Net/Total/Discount للفاتورة فتضعه بمقاييس مختلفة:
                                // netAmount كان يشمل الضريبة وtotalSales كان بعد الخصم
                                // والخصم كان مستوى الفاتورة فقط دون خصوم البنود
                                // (num2 كانت تُحسب ولا تُستعمل).
                                pos_document.totalSales = salesTotalSum;
                                pos_document.totalCommercialDiscount = decimal.Add(itemsDiscountSum, new decimal(invoice.Discount));
                                pos_document.netAmount = netSaleSum;
                                pos_document.totalAmount = lineTotalSum;
                                pos_document.paymentMethod = "C";
                                if (invoice.PayType == 2)
                                {
                                        pos_document.paymentMethod = "V";
                                }
                                pos_document.feesAmount = 0m;
                                pos_document.sOrderNameCode = "";
                                pos_document.orderdeliveryMode = "FC";
                                List<invoice_total_taxes> list2;
                                list2 = new List<invoice_total_taxes>();
                                try
                                {
                                        // P6-018 fix: مجاميع الضرايب من البنود نفسها (كانت من
                                        // حقلي الفاتورة) — تُطابق taxelists البنود حرفيًا.
                                        if (decimal.Compare(vatSum, 0m) > 0)
                                        {
                                                list2.Add(new invoice_total_taxes
                                                {
                                                        taxType = "T1",
                                                        amount = vatSum
                                                });
                                        }
                                }
                                catch (Exception projectError)
                                {
                                        ProjectData.SetProjectError(projectError);
                                        ProjectData.ClearProjectError();
                                }
                                try
                                {
                                        if (decimal.Compare(withholdingSum, 0m) > 0)
                                        {
                                                list2.Add(new invoice_total_taxes
                                                {
                                                        taxType = "T4",
                                                        amount = withholdingSum
                                                });
                                        }
                                }
                                catch (Exception projectError2)
                                {
                                        ProjectData.SetProjectError(projectError2);
                                        ProjectData.ClearProjectError();
                                }
                                pos_document.total_tax_lis = list2;
                                if ((object)customer != DBNull.Value && customer != null)
                                {
                                        Customer customer2;
                                        Customer customer3;
                                        customer2 = (customer3 = customer);
                                        string RegionName;
                                        RegionName = customer3.Region;
                                        Customer customer4;
                                        customer4 = (customer3 = customer);
                                        string CountryName;
                                        CountryName = customer3.Country;
                                        Customer customer5;
                                        customer5 = (customer3 = customer);
                                        string CityName;
                                        CityName = customer3.City;
                                        Common.GetCityName(ref RegionName, ref CountryName, ref CityName, customer.Region, customer.Country, customer.City);
                                        customer5.City = CityName;
                                        customer4.Country = CountryName;
                                        customer2.Region = RegionName;
                                }
                                buyer.id = customer.VATno;
                                buyer.mobileNumber = customer.Mobile;
                                buyer.name = customer.Name;
                                if ((customer.VATno == null) | ((object)customer.VATno == DBNull.Value) | (Operators.CompareString(customer.VATno.ToString(), "", TextCompare: false) == 0))
                                {
                                        buyer.type = "P";
                                        object obj;
                                        obj = customer.NatianalID ?? "";
                                        if (obj == null)
                                        {
                                                obj = "";
                                        }
                                        buyer.id = (string)obj;
                                }
                                else
                                {
                                        buyer.type = "B";
                                        object obj2;
                                        obj2 = customer.VATno ?? "";
                                        if (obj2 == null)
                                        {
                                                obj2 = "";
                                        }
                                        buyer.id = (string)obj2;
                                }
                                if (Common.FoundationInfoDT.Rows.Count > 0)
                                {
                                        pos_seller.rin = Conversions.ToString(RuntimeHelpers.GetObjectValue(Common.FoundationInfoDT.Rows[0]["tax_no"]));
                                        pos_seller.companyTradeName = Conversions.ToString(RuntimeHelpers.GetObjectValue(Common.FoundationInfoDT.Rows[0]["nameA"]));
                                        pos_seller.country = "EG";
                                        pos_seller.governate = Conversions.ToString(RuntimeHelpers.GetObjectValue(Operators.ConcatenateObject(Operators.ConcatenateObject("", Common.FoundationInfoDT.Rows[0]["Area"]), "")));
                                        pos_seller.regionCity = Conversions.ToString(RuntimeHelpers.GetObjectValue(Operators.ConcatenateObject(Operators.ConcatenateObject("", Common.FoundationInfoDT.Rows[0]["city"]), "")));
                                        pos_seller.street = Conversions.ToString(RuntimeHelpers.GetObjectValue(Operators.ConcatenateObject(Operators.ConcatenateObject("", Common.FoundationInfoDT.Rows[0]["StreetName"]), "")));
                                        pos_seller.buildingNumber = Conversions.ToString(RuntimeHelpers.GetObjectValue(Operators.ConcatenateObject(Operators.ConcatenateObject("", Common.FoundationInfoDT.Rows[0]["BuildingNumber"]), "")));
                                        pos_seller.postalCode = Conversions.ToString(RuntimeHelpers.GetObjectValue(Operators.ConcatenateObject(Operators.ConcatenateObject("", Common.FoundationInfoDT.Rows[0]["PostalZone"]), "")));
                                        pos_seller.floor = Conversions.ToString(RuntimeHelpers.GetObjectValue(Operators.ConcatenateObject(Operators.ConcatenateObject("", Common.FoundationInfoDT.Rows[0]["PostalZone"]), "")));
                                        pos_seller.room = "";
                                        pos_seller.device_serial = EtaSetting.PosEtaSerial;
                                        pos_seller.activityCode = EtaSetting.ActivityCode;
                                        pos_seller.branchCode = EtaSetting.BranchCode;
                                        send_respons_model send_respons_model;
                                        send_respons_model = await SendRecipt.send_recipt(pos_document, buyer, pos_seller, list, calc_uuid: true);
                                        // P6-017 fix: عقد النتيجة — true فقط عند القبول الصريح
                                        // (status=200) الذي يُثبت UUID في المستند؛ الرفض أو أي
                                        // استجابة أخرى = false فلا تختم المتابعة الفاتورة
                                        // «مرسلة» — كان يعيد true لأي رد غير استثنائي ثم
                                        // تُعلّم الشاشة الفاتورة ZatcaSent=1 رغم رفضها.
                                        if (send_respons_model != null && Operators.CompareString(send_respons_model.status, "200", TextCompare: false) == 0)
                                        {
                                                new InvoiceOper().UpdateInvoiceStatus(invoice.InvGlobalID, send_respons_model.uuid);
                                                return true;
                                        }
                                        return false;
                                }
                                if (Operators.CompareString(MainClass.Language, "ar", TextCompare: false) == 0)
                                {
                                        Interaction.MsgBox("الرجاء ادخال بيانات المنشأة");
                                }
                                else
                                {
                                        Interaction.MsgBox("Please enter foundation data!");
                                }
                                return false;
                        }
                        catch (Exception projectError4)
                        {
                                ProjectData.SetProjectError(projectError4);
                                bool result;
                                result = false;
                                ProjectData.ClearProjectError();
                                return result;
                        }
                }

                public void Generate_QR(string mycompanyname, string mycompanyname_Tax_No, string InvNo, DateTime InvDate, double InvTax, double InvTotal)
                {
                        try
                        {
                                Console.WriteLine(new QRCode(new QRCodeGenerator().CreateQrCode("الشركة : " + mycompanyname + "\r\nVAT : " + mycompanyname_Tax_No + "\r\nرقم الفاتورة : " + Conversions.ToString(InvDate) + "\r\nالتاريخ : " + Strings.Format(InvDate, "yyyy-MM-dd") + " " + Strings.Format(DateAndTime.TimeOfDay, "HH:mm:ss").ToString() + "\r\nالاجمالى : " + Conversions.ToString(InvTax) + "\r\nالضريبة : " + Conversions.ToString(InvTotal), QRCodeGenerator.ECCLevel.Q)));
                        }
                        catch (Exception projectError)
                        {
                                ProjectData.SetProjectError(projectError);
                                ProjectData.ClearProjectError();
                        }
                }
        }
}