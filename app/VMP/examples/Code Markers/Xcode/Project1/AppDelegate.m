//
//  AppDelegate.m
//  Project1
//
//  Created by vano on 17.07.14.
//  Copyright (c) 2014 ___FULLUSERNAME___. All rights reserved.
//

#import "AppDelegate.h"
#import "VMProtectSDK.h"

@implementation AppDelegate
@synthesize txtPsw;

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [_window center];
}

- (IBAction)CheckPassword:(id)sender {
    VMProtectBegin("Test marker");
    int pwd = self.txtPsw.intValue;
    BOOL correct = (13 == (pwd % 17));
    NSAlert *alert = [[NSAlert alloc] init];
    [alert addButtonWithTitle:@"OK"];
    [alert setMessageText: correct ? @"Information" : @"Error"];
    NSString *msg = [[NSString alloc] initWithUTF8String: correct ?
                     VMProtectDecryptStringA("Correct password") :
                     VMProtectDecryptStringA("Incorrect password")];
    [alert setInformativeText: msg];
    [alert setAlertStyle: correct ? NSInformationalAlertStyle : NSWarningAlertStyle];
    [alert runModal];
    VMProtectEnd();
}

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)theApplication {
    return YES;
}

@end
