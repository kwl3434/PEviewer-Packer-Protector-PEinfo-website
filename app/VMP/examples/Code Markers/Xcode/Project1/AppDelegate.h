//
//  AppDelegate.h
//  Project1
//
//  Created by vano on 17.07.14.
//  Copyright (c) 2014 ___FULLUSERNAME___. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface AppDelegate : NSObject <NSApplicationDelegate>

@property (assign) IBOutlet NSWindow *window;
- (IBAction)CheckPassword:(id)sender;
@property (weak) IBOutlet NSSecureTextField *txtPsw;

@end
