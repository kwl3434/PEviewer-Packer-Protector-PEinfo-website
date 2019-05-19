using System;
using System.Windows.Forms;

namespace Project1
{
	public partial class Form1 : Form
	{
		public Form1()
		{
			InitializeComponent();
		}

		private bool CheckPassword(string pwd)
		{
			UInt64 magicNum;
			return (UInt64.TryParse(pwd, out magicNum) && magicNum % 17 == 13);
		}

		[VMProtect.Begin]
		private void btnCheckPassword_Click(object sender, EventArgs e)
		{
			if (CheckPassword(txtPassword.Text))
			{
				MessageBox.Show(VMProtect.SDK.DecryptString("Correct password"), VMProtect.SDK.DecryptString("Password check"), MessageBoxButtons.OK, MessageBoxIcon.Information);
			} else
			{
				MessageBox.Show(VMProtect.SDK.DecryptString("Incorrect password"), VMProtect.SDK.DecryptString("Password check"), MessageBoxButtons.OK, MessageBoxIcon.Error);
				txtPassword.Focus();
			}
		}
	}
}
