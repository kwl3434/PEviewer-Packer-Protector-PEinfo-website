#import "AppDelegate.h"
#import "VMProtectSDK.h"

@implementation AppDelegate

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender
{
	return YES;
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
	int nSize = VMProtectGetCurrentHWID(NULL, 0);
	char *p = new char[nSize];
	VMProtectGetCurrentHWID(p, nSize);
	
	self.hwid.stringValue = [NSString stringWithUTF8String:p];
	
	delete [] p;
}

#define APPEND_FLAG(flag) if ((res & flag) == flag) { str = [str stringByAppendingFormat:@"%s\n", #flag]; }

- (void)controlTextDidChange:(NSNotification *)notification
{
	NSString *serial = [notification.object stringValue];
	int res = VMProtectSetSerialNumber(serial.UTF8String);
	
	if (res != 0)
	{
		NSString *str = @"";
		
		APPEND_FLAG(SERIAL_STATE_FLAG_CORRUPTED);
		APPEND_FLAG(SERIAL_STATE_FLAG_INVALID);
		APPEND_FLAG(SERIAL_STATE_FLAG_BLACKLISTED);
		APPEND_FLAG(SERIAL_STATE_FLAG_DATE_EXPIRED);
		APPEND_FLAG(SERIAL_STATE_FLAG_RUNNING_TIME_OVER);
		APPEND_FLAG(SERIAL_STATE_FLAG_BAD_HWID);
		APPEND_FLAG(SERIAL_STATE_FLAG_MAX_BUILD_EXPIRED);
		
		self.results.stringValue = str;
		return;
	}

	VMProtectSerialNumberData data = {};
	BOOL res2 = VMProtectGetSerialNumberData(&data, sizeof(data));
	if (!res2)
	{
		self.results.stringValue = @"VMProtectGetSerialNumberData() returned FALSE";
		return;
	}

	NSString *strLog = @"";
	if (data.wUserName[0])
		strLog = [strLog stringByAppendingFormat:@"Name: %@\n", [[NSString alloc] initWithBytes:data.wUserName length:sizeof(data.wUserName) encoding:NSUTF16LittleEndianStringEncoding]];
	if (data.wEMail[0])
		strLog = [strLog stringByAppendingFormat:@"Email: %@\n", [[NSString alloc] initWithBytes:data.wEMail length:sizeof(data.wEMail) encoding:NSUTF16LittleEndianStringEncoding]];
	if (data.dtExpire.wYear)
		strLog = [strLog stringByAppendingFormat:@"Expires at: %02d/%02d/%04d\n", data.dtExpire.bDay, data.dtExpire.bMonth, data.dtExpire.wYear];
	if (data.dtMaxBuild.wYear)
		strLog = [strLog stringByAppendingFormat:@"Updates end at: %02d/%02d/%04d\n", data.dtMaxBuild.bDay, data.dtMaxBuild.bMonth, data.dtMaxBuild.wYear];
	if (data.bRunningTime)
		strLog = [strLog stringByAppendingFormat:@"Running time limit: %d seconds\n", data.bRunningTime];
	if (data.nUserDataLength > 0)
		strLog = [strLog stringByAppendingFormat:@"User data length: %d bytes\n", data.nUserDataLength];
		
	self.results.stringValue = strLog;
}

- (void) runProtectedCode:(id)sender
{
	VMProtectBeginVirtualizationLockByKey("locked");
	
	NSRunAlertPanel(@"Protected Code", @"This code will not work without a valid serial number", @"OK", nil, nil);

	VMProtectEnd();
}

@end
