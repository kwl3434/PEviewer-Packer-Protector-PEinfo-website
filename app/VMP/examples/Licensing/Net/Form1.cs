using System;
using System.Windows.Forms;

namespace TestApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        [VMProtect.BeginVirtualizationLockByKey]
        private void cmdExecProtectedCode_Click(object sender, EventArgs e)
        {
            MessageBox.Show(@"Protected code successfully executed", @"ProtectedCode()", MessageBoxButtons.OK,
                MessageBoxIcon.Information);
        }

        private void cmdClose_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            txtHwid.Text = VMProtect.SDK.GetCurrentHWID();
        }

        private void AppendResultLine(string fmt, params object[] args)
        {
            var value = string.Format(fmt, args);
            if (txtResult.Text.Length == 0)
                txtResult.Text = value;
            else
                txtResult.AppendText("\r\n" + value);
        }
        private void txtSerial_TextChanged(object sender, EventArgs e)
        {
            var status = VMProtect.SDK.SetSerialNumber(txtSerial.Text);
            txtResult.Clear();
            AppendResultLine("VMProtectSetSerialNumber() returned: {0}", status);
            AppendResultLine("");

            var status2 = VMProtect.SDK.GetSerialNumberState();
            AppendResultLine("VMProtectGetSerialNumberState() returned: {0}", status2);
            AppendResultLine("");

            VMProtect.SerialNumberData sd;
            var res = VMProtect.SDK.GetSerialNumberData(out sd);
            AppendResultLine("VMProtectGetSerialNumberData() returned: {0}", res);
            if (res)
            {
                AppendResultLine("State = {0}", sd.State);
                AppendResultLine("User Name = {0}", sd.UserName);
                AppendResultLine("E-Mail = {0}", sd.EMail);
                AppendResultLine("Date of expiration = {0}", sd.Expires);
                AppendResultLine("Max date of build = {0}", sd.MaxBuild);
                AppendResultLine("Running time limit = {0} minutes", sd.RunningTime);
                AppendResultLine("Length of user data = {0} bytes", sd.UserData.Length);
            }
        }
    }
}
