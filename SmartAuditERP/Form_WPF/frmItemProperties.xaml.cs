using DevExpress.Xpf.Core;
using System;
using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmItemProperties : ThemedWindow
    {
        #region Fields

        public int ItemProperty;
        public double NetQnty;
        private bool _isInternalUpdate;
        // The editable packing request is not the multiplied output.
        private string _packingInputText;
        private bool _packingRoundUp;
        private bool _packingHeightEdited;

        #endregion

        #region Constructor

        public frmItemProperties()
        {
            ItemProperty = 1;
            NetQnty = 0.0;
            InitializeComponent();
        }

        #endregion

        #region Load

        private void frmItemProperties_Load(object sender, RoutedEventArgs e)
        {
            try
            {
                if (cmbItemProperties.Items.Count > 0)
                {
                    if (ItemProperty >= 1 && ItemProperty <= cmbItemProperties.Items.Count)
                        cmbItemProperties.SelectedIndex = ItemProperty - 1;
                    else
                        cmbItemProperties.SelectedIndex = 0;
                }

                if (string.IsNullOrWhiteSpace(txtHeight.Text))
                    txtHeight.Text = "0";

                if (string.IsNullOrWhiteSpace(txtWidth.Text))
                    txtWidth.Text = "0";

                if (string.IsNullOrWhiteSpace(txtQty.Text))
                    txtQty.Text = "1";

                if (NetQnty > 0 && string.IsNullOrWhiteSpace(txtNetQnty.Text))
                    txtNetQnty.Text = FormatNumber(NetQnty);
                else if (string.IsNullOrWhiteSpace(txtNetQnty.Text))
                    txtNetQnty.Text = "0";

                ApplyPropertyMode();
                Calc();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region Helpers

        private void ApplyPropertyMode()
        {
            if (cmbItemProperties.SelectedIndex >= 0)
                ItemProperty = cmbItemProperties.SelectedIndex + 1;

            bool isPacking = (ItemProperty == 2);
            txtNetQnty.IsReadOnly = !isPacking;
        }

        private double ParseNumber(string text, double defaultValue = 0)
        {
            if (string.IsNullOrWhiteSpace(text))
                return defaultValue;

            string normalized = text.Trim().Replace("٫", ".").Replace(",", ".");

            if (double.TryParse(normalized, NumberStyles.Any, CultureInfo.InvariantCulture, out double result))
                return result;

            if (double.TryParse(text, NumberStyles.Any, CultureInfo.CurrentCulture, out double result2))
                return result2;

            return defaultValue;
        }

        private string FormatNumber(double value)
        {
            if (Math.Abs(value % 1) < 0.0000001)
                return Math.Round(value).ToString(CultureInfo.InvariantCulture);

            return value.ToString("0.###", CultureInfo.InvariantCulture);
        }

        private void SetTextSilently(TextBox textBox, string value)
        {
            _isInternalUpdate = true;
            textBox.Text = value;
            _isInternalUpdate = false;
        }

        private void FocusAndSelect(TextBox textBox)
        {
            textBox.Focus();
            textBox.SelectAll();
        }

        #endregion

        #region Calc

        private void Calc()
        {
            if (_isInternalUpdate)
                return;

            try
            {
                _isInternalUpdate = true;

                if (string.IsNullOrWhiteSpace(txtWidth.Text))
                    txtWidth.Text = "0";

                if (string.IsNullOrWhiteSpace(txtHeight.Text))
                    txtHeight.Text = "0";

                if (string.IsNullOrWhiteSpace(txtQty.Text))
                    txtQty.Text = "1";

                double widthValue = ParseNumber(txtWidth.Text, 0);
                double heightValue = ParseNumber(txtHeight.Text, 0);
                double qtyValue = ParseNumber(txtQty.Text, 1);
                double netQntyValue = ParseNumber(txtNetQnty.Text, 0);

                if (ItemProperty == 2) // تعبئة
                {
                    if (_packingInputText == null)
                        _packingInputText = txtNetQnty.Text;
                    netQntyValue = ParseNumber(_packingInputText, 0);

                    if (widthValue <= 0 || qtyValue <= 0)
                    {
                        heightValue = 0;
                        netQntyValue = 0;
                    }
                    else
                    {
                        heightValue = _packingRoundUp
                            ? Math.Ceiling(netQntyValue / widthValue)
                            : netQntyValue / widthValue;

                        netQntyValue = heightValue * widthValue * qtyValue;
                    }

                    txtHeight.Text = FormatNumber(heightValue);
                    txtNetQnty.Text = FormatNumber(netQntyValue);
                }
                else if (ItemProperty == 3) // مساحة
                {
                    netQntyValue = heightValue * widthValue * qtyValue;
                    txtNetQnty.Text = FormatNumber(netQntyValue);
                }
                else if (ItemProperty == 4) // متر طولي
                {
                    netQntyValue = ((2.0 * heightValue) + (2.0 * widthValue)) * qtyValue;
                    txtNetQnty.Text = FormatNumber(netQntyValue);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "خطأ حساب", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                _isInternalUpdate = false;
            }
        }

        #endregion

        #region TextChanged Events

        private void txtHeight_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_isInternalUpdate) return;

            double height = ParseNumber(txtHeight.Text, 0);
            _packingRoundUp = Math.Abs(height % 1.0) >= 0.0000001;
            if (ItemProperty == 2) _packingHeightEdited = true;
            if (!string.IsNullOrWhiteSpace(txtHeight.Text) && ItemProperty != 2)
                Calc();
        }

        private void txtWidth_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_isInternalUpdate) return;

            if (!string.IsNullOrWhiteSpace(txtWidth.Text) && ItemProperty != 2)
                Calc();
        }

        private void txtQty_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_isInternalUpdate) return;

            if (!string.IsNullOrWhiteSpace(txtQty.Text))
                Calc();
        }

        private void txtNetQnty_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (!_isInternalUpdate && ItemProperty == 2)
                _packingInputText = txtNetQnty.Text;
        }

        #endregion

        #region LostFocus Events

        private void txtHeight_Leave(object sender, RoutedEventArgs e)
        {
            try
            {
                double heightValue = ParseNumber(txtHeight.Text, 0);
                double widthValue = ParseNumber(txtWidth.Text, 0);
                if (ItemProperty != 2 || _packingHeightEdited)
                {
                    string requested = FormatNumber(heightValue * widthValue);
                    if (ItemProperty == 2)
                    {
                        _packingInputText = requested;
                        _packingHeightEdited = false;
                    }
                    SetTextSilently(txtNetQnty, requested);
                }
                Calc();
            }
            catch { }
        }

        private void txtQty_Leave(object sender, RoutedEventArgs e)
        {
            try { Calc(); } catch { }
        }

        private void txtNetQnty_Leave(object sender, RoutedEventArgs e)
        {
            try { Calc(); } catch { }
        }

        #endregion

        #region KeyDown Events

        private void txtHeight_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                double heightValue = ParseNumber(txtHeight.Text, 0);
                double widthValue = ParseNumber(txtWidth.Text, 0);
                if (ItemProperty != 2 || _packingHeightEdited)
                {
                    string requested = FormatNumber(heightValue * widthValue);
                    if (ItemProperty == 2)
                    {
                        _packingInputText = requested;
                        _packingHeightEdited = false;
                    }
                    SetTextSilently(txtNetQnty, requested);
                }
                Calc();
                FocusAndSelect(txtWidth);
                e.Handled = true;
            }
        }

        private void txtWidth_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                Calc();
                btnInsert.Focus();
                e.Handled = true;
            }
        }

        private void txtQty_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                Calc();
                e.Handled = true;
            }
        }

        private void txtNetQnty_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                Calc();
                btnInsert.Focus();
                e.Handled = true;
            }
        }

        #endregion

        #region Button / ComboBox Events

        private void btnInsert_Click(object sender, RoutedEventArgs e)
        {
            Calc();
            NetQnty = ParseNumber(txtNetQnty.Text, 0);
            try { DialogResult = true; } catch { }
            Close();
        }

        private void cmbItemProperties_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            // Do not reuse an earlier packing request after a mode switch.
            _packingInputText = null;
            _packingHeightEdited = false;
            ApplyPropertyMode();
            Calc();
        }

        #endregion
    }
}