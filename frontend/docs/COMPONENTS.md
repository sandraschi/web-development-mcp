# UI Components Documentation

This document provides an overview of the reusable UI components available in the application.

## Table of Contents

- [Button](#button)
- [Card](#card)
- [Input](#input)
- [Tabs](#tabs)
- [Dropdown Menu](#dropdown-menu)
- [Select](#select)
- [Switch](#switch)
- [Label](#label)
- [Badge](#badge)
- [Separator](#separator)

## Button

A customizable button component with various styles and states.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'` | `'default'` | The visual style of the button |
| `size` | `'default' | 'sm' | 'lg' | 'icon'` | `'default'` | The size of the button |
| `asChild` | `boolean` | `false` | Render as child component |
| `loading` | `boolean` | `false` | Show loading state |
| `leftIcon` | `React.ReactNode` | - | Icon to display on the left |
| `rightIcon` | `React.ReactNode` | - | Icon to display on the right |
| All other props | `React.ButtonHTMLAttributes<HTMLButtonElement>` | - | Standard button props |

### Examples

```tsx
// Default button
<Button>Click me</Button>

// Outline button with icon
<Button variant="outline">
  <Plus className="mr-2 h-4 w-4" />
  Add Item
</Button>

// Loading state
<Button loading>Processing...</Button>

// Icon button
<Button variant="ghost" size="icon">
  <Settings className="h-4 w-4" />
</Button>
```

## Card

A flexible card component with header, content, and footer sections.

### Subcomponents

- `Card`: The root card component
- `CardHeader`: Container for the card header
- `CardTitle`: Card title
- `CardDescription`: Card description
- `CardContent`: Main card content
- `CardFooter`: Card footer content

### Example

```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card Description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content goes here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

## Input

A styled input component with support for various types and states.

### Props

All standard HTML input props are supported, plus:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |

### Example

```tsx
<Input
  type="text"
  placeholder="Enter your name"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

## Tabs

A tabbed interface component.

### Subcomponents

- `Tabs`: The root tabs component
- `TabsList`: Container for tab triggers
- `TabsTrigger`: Individual tab trigger
- `TabsContent`: Content for each tab

### Example

```tsx
<Tabs defaultValue="account" className="w-[400px]">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">
    <p>Account settings</p>
  </TabsContent>
  <TabsContent value="password">
    <p>Password settings</p>
  </TabsContent>
</Tabs>
```

## Dropdown Menu

A dropdown menu component for displaying a list of actions or options.

### Subcomponents

- `DropdownMenu`: The root dropdown menu component
- `DropdownMenuTrigger`: The button that toggles the dropdown
- `DropdownMenuContent`: The content of the dropdown
- `DropdownMenuItem`: An item in the dropdown
- `DropdownMenuLabel`: A label for a group of items
- `DropdownMenuSeparator`: A visual separator
- `DropdownMenuCheckboxItem`: A menu item with a checkbox
- `DropdownMenuRadioGroup`: A group of radio items
- `DropdownMenuRadioItem`: A menu item with a radio button
- `DropdownMenuSub`: A submenu
- `DropdownMenuSubTrigger`: The trigger for a submenu
- `DropdownMenuSubContent`: The content of a submenu
- `DropdownMenuShortcut`: A keyboard shortcut hint

### Example

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Open</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>My Account</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Profile</DropdownMenuItem>
    <DropdownMenuItem>Billing</DropdownMenuItem>
    <DropdownMenuItem>Team</DropdownMenuItem>
    <DropdownMenuItem>Subscription</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Select

A styled select component.

### Subcomponents

- `Select`: The root select component
- `SelectTrigger`: The button that toggles the select
- `SelectValue`: The value displayed in the trigger
- `SelectContent`: The content of the select
- `SelectItem`: An item in the select
- `SelectGroup`: A group of items
- `SelectLabel`: A label for a group of items
- `SelectSeparator`: A visual separator
- `SelectScrollUpButton`: A button to scroll up
- `SelectScrollDownButton`: A button to scroll down

### Example

```tsx
<Select>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>
  <SelectContent>
    <SelectGroup>
      <SelectLabel>Fruits</SelectLabel>
      <SelectItem value="apple">Apple</SelectItem>
      <SelectItem value="banana">Banana</SelectItem>
      <SelectItem value="orange">Orange</SelectItem>
    </SelectGroup>
  </SelectContent>
</Select>
```

## Switch

A toggle switch component.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | `boolean` | - | Whether the switch is checked |
| `onCheckedChange` | `(checked: boolean) => void` | - | Callback when checked state changes |
| `disabled` | `boolean` | `false` | Whether the switch is disabled |
| `className` | `string` | - | Additional CSS classes |

### Example

```tsx
<Switch 
  checked={enabled} 
  onCheckedChange={setEnabled} 
  className="data-[state=checked]:bg-green-500"
/>
```

## Label

A form label component.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `htmlFor` | `string` | - | The ID of the form element the label is for |
| `className` | `string` | - | Additional CSS classes |

### Example

```tsx
<div className="flex flex-col space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
</div>
```

## Badge

A small status badge component.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning' | 'error' | 'info'` | `'default'` | The visual style of the badge |
| `className` | `string` | - | Additional CSS classes |

### Example

```tsx
<Badge variant="outline">New</Badge>
<Badge variant="success">Active</Badge>
<Badge variant="destructive">Error</Badge>
```

## Separator

A horizontal or vertical divider.

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `'horizontal' | 'vertical'` | `'horizontal'` | The orientation of the separator |
| `className` | `string` | - | Additional CSS classes |

### Example

```tsx
<div>
  <div>Content above</div>
  <Separator className="my-4" />
  <div>Content below</div>
</div>
```
