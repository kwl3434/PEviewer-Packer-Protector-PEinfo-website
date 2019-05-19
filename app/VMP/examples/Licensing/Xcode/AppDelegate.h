@interface AppDelegate : NSObject <NSApplicationDelegate>

@property (assign) IBOutlet NSWindow *window;
@property (assign) IBOutlet NSTextField *results;
@property (assign) IBOutlet NSTextField *hwid;

- (IBAction)runProtectedCode:(id)sender;

@end
