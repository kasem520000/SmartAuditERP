using System.Windows;

namespace SmartAuditERP.Form_WPF
{
    public partial class MsgExistItem : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        public int Action = 0;

        #endregion

        #region Constructor

        public MsgExistItem()
        {
            InitializeComponent();
            Action = 0;
        }

        #endregion

        #region Window Load

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            // لا شيء مطلوب عند التحميل
        }

        #endregion

        #region Button Events

        private void btnAddquantity_Click(object sender, RoutedEventArgs e)
        {
            this.Topmost = false;
            // P7-143 fix: القيمتان معكوستان عند كل المستهلكين — إضافة الكمية
            // هي Action=1 (يرفعون كمية السطر القائم) والإدراج في بند جديد
            // هو Action=2 (يضيفون سطراً)؛ الحوار كان يعكسهما فيؤدي كل زر
            // عكس معناه المكتوب عليه
            Action = 1;
            this.Hide();
        }

        private void btnNewTirm_Click(object sender, RoutedEventArgs e)
        {
            this.Topmost = false;
            // P7-143: بند جديد = 2 عند كل المستهلكين (يكملون إلى إدراج سطر)
            Action = 2;
            this.Hide();
        }

        private void btnNon_Click(object sender, RoutedEventArgs e)
        {
            this.Topmost = false;
            Action = 3;
            this.Hide();
        }

        #endregion
    }
}