import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../button';
import { Plus } from 'lucide-react';

describe('Button', () => {
  it('renders a button with default variant and size', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-primary');
    expect(button).toHaveClass('text-primary-foreground');
    expect(button).toHaveClass('h-10');
    expect(button).toHaveClass('px-4');
  });

  it('renders a button with outline variant', () => {
    render(<Button variant="outline">Outline Button</Button>);
    const button = screen.getByRole('button', { name: /outline button/i });
    
    expect(button).toHaveClass('border');
    expect(button).toHaveClass('border-input');
    expect(button).toHaveClass('bg-background');
  });

  it('renders a small button', () => {
    render(<Button size="sm">Small Button</Button>);
    const button = screen.getByRole('button', { name: /small button/i });
    
    expect(button).toHaveClass('h-9');
    expect(button).toHaveClass('px-3');
    expect(button).toHaveClass('rounded-md');
  });

  it('renders a button with an icon', () => {
    render(
      <Button>
        <Plus className="mr-2 h-4 w-4" />
        Add Item
      </Button>
    );
    
    const button = screen.getByRole('button', { name: /add item/i });
    const icon = button.querySelector('svg');
    
    expect(icon).toBeInTheDocument();
    expect(icon).toHaveClass('h-4 w-4');
    expect(icon).toHaveClass('mr-2');
  });

  it('shows loading state', () => {
    render(<Button loading>Loading...</Button>);
    const button = screen.getByRole('button', { name: /loading/i });
    const loader = button.querySelector('svg.animate-spin');
    
    expect(loader).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('renders as a link when asChild is true', () => {
    render(
      <Button asChild>
        <a href="https://example.com">Link Button</a>
      </Button>
    );
    
    const link = screen.getByRole('link', { name: /link button/i });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', 'https://example.com');
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Custom Styled</Button>);
    const button = screen.getByRole('button', { name: /custom styled/i });
    
    expect(button).toHaveClass('custom-class');
  });

  it('is disabled when loading is true', () => {
    render(<Button loading>Loading Button</Button>);
    const button = screen.getByRole('button', { name: /loading button/i });
    
    expect(button).toBeDisabled();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled Button</Button>);
    const button = screen.getByRole('button', { name: /disabled button/i });
    
    expect(button).toBeDisabled();
    expect(button).toHaveClass('opacity-50');
    expect(button).toHaveClass('pointer-events-none');
  });

  it('renders with left and right icons', () => {
    render(
      <Button leftIcon={<Plus data-testid="left-icon" />} rightIcon={<Plus data-testid="right-icon" />}>
        With Icons
      </Button>
    );
    
    const button = screen.getByRole('button', { name: /with icons/i });
    const leftIcon = screen.getByTestId('left-icon');
    const rightIcon = screen.getByTestId('right-icon');
    
    expect(leftIcon).toBeInTheDocument();
    expect(rightIcon).toBeInTheDocument();
    expect(button.firstChild).toContainElement(leftIcon);
    expect(button.lastChild).toContainElement(rightIcon);
  });
});
