using DevExpress.Xpf.Core;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows;

namespace SmartAuditERP.Form_WPF
{
    public partial class FrmSallah : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SallaAPI sallaApi;
        private ProductsManager productsManager;
        private OrdersManager ordersManager;

        #endregion

        #region Constructor

        public FrmSallah()
        {
            InitializeComponent();
        }

        #endregion

        #region Window Loaded

        private async void Window_Loaded(object sender, RoutedEventArgs e)
        {
            sallaApi         = new SallaAPI("2adcaba8-c5a8-426c-8fc9-3281fa4b056d");
            productsManager  = new ProductsManager(sallaApi);
            ordersManager    = new OrdersManager(sallaApi);
        }

        #endregion

        #region Button Events

        private async void btnGetProducts_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var result = await productsManager.GetProducts();
                // P6-030 fix: العدد من بيانات ترقيم الخدمة (pagination.total) لا من
                // عدّ عناصر الصفحة الأولى — كان العرض يقول «X منتج» وX عدد صفحة
                // واحدة فقط.
                int count = ExtractTotalCount(result, fallback: result["data"].ToObject<List<object>>().Count);
                DXMessageBox.Show($"إجمالي المنتجات (وفق ترقيم سلة): {count}.", "نجح",
                                MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ: {ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async void btnGetOrders_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var result = await ordersManager.GetOrders();
                // P6-030 fix: نفس عقد العدد من الترقيم الكلي لا من الصفحة الأولى
                int count = ExtractTotalCount(result, fallback: result["data"].ToObject<List<object>>().Count);
                DXMessageBox.Show($"إجمالي الطلبات (وفق ترقيم سلة): {count}.", "نجح",
                                MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ: {ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        // P6-030 fix: استخراج الإجمالي من كائن pagination في رد سلة (total)،
        // وإلا فعدد العناصر المعاد كخطة بديلة.
        private static int ExtractTotalCount(JObject result, int fallback)
        {
            try
            {
                JToken total = result?["pagination"]?["total"];
                if (total != null)
                {
                    return (int)total;
                }
            }
            catch
            {
            }
            return fallback;
        }

        private async void btnAddProduct_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // P6-030 fix: الزر كان يُنشئ منتجًا ثابتًا (اسم/سعر/كمية صلبة) في
                // المتجر الحقيقي بمجرد نقرة — تأكيد صريح بأن هذا إنشاء عينة
                // فعلية في المتجر قبل التنفيذ.
                if (DXMessageBox.Show(
                        "سيُنشأ منتج عينة بالبيانات الثابتة في متجر سلة الفعلي — متابعة؟",
                        "تأكيد إنشاء عينة", MessageBoxButton.YesNo, MessageBoxImage.Question)
                    != MessageBoxResult.Yes)
                {
                    return;
                }

                var productData = new
                {
                    name        = "اسم المنتج",
                    price       = 100,
                    quantity    = 50,
                    description = "وصف المنتج"
                };

                await productsManager.CreateProduct(productData);
                DXMessageBox.Show("تم إضافة المنتج بنجاح.", "نجح",
                                MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ: {ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async void Button3_Click(object sender, RoutedEventArgs e)
        {
            // نفس منطق جلب الطلبات
            await Task.Run(() => { });
            DXMessageBox.Show("جلب الطلبات (2) — يمكن تخصيصه لاحقاً.", "تنبيه",
                            MessageBoxButton.OK, MessageBoxImage.Information);
        }

        #endregion
    }
}