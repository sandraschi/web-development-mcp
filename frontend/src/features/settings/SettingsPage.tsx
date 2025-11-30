import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import { useTheme } from '@/providers/theme-provider';

type Theme = 'light' | 'dark' | 'system';

export default function SettingsPage() {
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const { theme, setTheme } = useTheme();
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    notifications: {
      email: true,
      push: true,
      newsletter: false,
    },
    appearance: {
      theme: theme as Theme,
      fontSize: '16px',
      compactMode: false,
    },
    security: {
      twoFactorAuth: false,
      sessionTimeout: 30,
    },
  });

  // Simulate loading user settings
  useEffect(() => {
    const timer = setTimeout(() => {
      // In a real app, this would be an API call
      setFormData(prev => ({
        ...prev,
        name: 'John Doe',
        email: 'john.doe@example.com',
        company: 'Acme Inc.',
      }));
      setIsLoading(false);
    }, 800);

    return () => clearTimeout(timer);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent as keyof typeof prev],
          [child]: type === 'checkbox' ? checked : value,
        },
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
    }
  };

  const handleThemeChange = (value: string) => {
    const newTheme = value as Theme;
    setTheme(newTheme);
    setFormData(prev => ({
      ...prev,
      appearance: {
        ...prev.appearance,
        theme: newTheme,
      },
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    
    // Simulate API call
    setTimeout(() => {
      console.log('Settings saved:', formData);
      setIsSaving(false);
      // Show success toast here
    }, 1000);
  };

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-8rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      <Tabs defaultValue="general" className="space-y-4">
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="appearance">Appearance</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
        </TabsList>

        <form onSubmit={handleSubmit}>
          <TabsContent value="general" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Profile</CardTitle>
                <CardDescription>
                  Update your profile information and contact details.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="name">Full Name</Label>
                    <Input
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      disabled
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="company">Company</Label>
                  <Input
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleInputChange}
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="appearance" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Appearance</CardTitle>
                <CardDescription>
                  Customize the look and feel of the application.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="theme">Theme</Label>
                  <Select
                    value={formData.appearance.theme}
                    onValueChange={handleThemeChange}
                  >
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder="Select theme" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="light">Light</SelectItem>
                      <SelectItem value="dark">Dark</SelectItem>
                      <SelectItem value="system">System</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="fontSize">Font Size</Label>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs">A</span>
                    <Input
                      id="fontSize"
                      name="appearance.fontSize"
                      type="range"
                      min="12"
                      max="24"
                      step="1"
                      value={parseInt(formData.appearance.fontSize)}
                      onChange={(e) => {
                        setFormData(prev => ({
                          ...prev,
                          appearance: {
                            ...prev.appearance,
                            fontSize: `${e.target.value}px`,
                          },
                        }));
                      }}
                      className="w-full max-w-[200px]"
                    />
                    <span className="text-lg">A</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Switch
                    id="compactMode"
                    checked={formData.appearance.compactMode}
                    onCheckedChange={(checked) => {
                      setFormData(prev => ({
                        ...prev,
                        appearance: {
                          ...prev.appearance,
                          compactMode: checked,
                        },
                      }));
                    }}
                  />
                  <Label htmlFor="compactMode">Compact Mode</Label>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Notifications</CardTitle>
                <CardDescription>
                  Configure how you receive notifications.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-4">
                  <div className="flex items-center justify-between space-x-2">
                    <div className="space-y-0.5">
                      <Label htmlFor="email-notifications">Email Notifications</Label>
                      <p className="text-sm text-muted-foreground">
                        Receive email notifications about your account activity.
                      </p>
                    </div>
                    <Switch
                      id="email-notifications"
                      checked={formData.notifications.email}
                      onCheckedChange={(checked) => {
                        setFormData(prev => ({
                          ...prev,
                          notifications: {
                            ...prev.notifications,
                            email: checked,
                          },
                        }));
                      }}
                    />
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between space-x-2">
                    <div className="space-y-0.5">
                      <Label htmlFor="push-notifications">Push Notifications</Label>
                      <p className="text-sm text-muted-foreground">
                        Receive push notifications in your browser.
                      </p>
                    </div>
                    <Switch
                      id="push-notifications"
                      checked={formData.notifications.push}
                      onCheckedChange={(checked) => {
                        setFormData(prev => ({
                          ...prev,
                          notifications: {
                            ...prev.notifications,
                            push: checked,
                          },
                        }));
                      }}
                    />
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between space-x-2">
                    <div className="space-y-0.5">
                      <Label htmlFor="newsletter">Newsletter</Label>
                      <p className="text-sm text-muted-foreground">
                        Subscribe to our newsletter for product updates.
                      </p>
                    </div>
                    <Switch
                      id="newsletter"
                      checked={formData.notifications.newsletter}
                      onCheckedChange={(checked) => {
                        setFormData(prev => ({
                          ...prev,
                          notifications: {
                            ...prev.notifications,
                            newsletter: checked,
                          },
                        }));
                      }}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="security" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Security</CardTitle>
                <CardDescription>
                  Manage your account security settings.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Two-Factor Authentication</Label>
                      <p className="text-sm text-muted-foreground">
                        Add an extra layer of security to your account.
                      </p>
                    </div>
                    <Switch
                      checked={formData.security.twoFactorAuth}
                      onCheckedChange={(checked) => {
                        setFormData(prev => ({
                          ...prev,
                          security: {
                            ...prev.security,
                            twoFactorAuth: checked,
                          },
                        }));
                      }}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="session-timeout">Session Timeout</Label>
                  <Select
                    value={formData.security.sessionTimeout.toString()}
                    onValueChange={(value) => {
                      setFormData(prev => ({
                        ...prev,
                        security: {
                          ...prev.security,
                          sessionTimeout: parseInt(value),
                        },
                      }));
                    }}
                  >
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder="Select timeout" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="15">15 minutes</SelectItem>
                      <SelectItem value="30">30 minutes</SelectItem>
                      <SelectItem value="60">1 hour</SelectItem>
                      <SelectItem value="120">2 hours</SelectItem>
                      <SelectItem value="0">Never</SelectItem>
                    </SelectContent>
                  </Select>
                  <p className="text-sm text-muted-foreground">
                    Automatically sign out after a period of inactivity.
                  </p>
                </div>
              </CardContent>
              <CardFooter className="border-t px-6 py-4">
                <Button type="submit" disabled={isSaving}>
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>
        </form>
      </Tabs>
    </div>
  );
}
