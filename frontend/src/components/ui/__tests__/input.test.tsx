import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Input } from '../input';

describe('Input', () => {
  it('renders an input element with default props', () => {
    render(<Input data-testid="input" />);
    const input = screen.getByTestId('input');
    
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute('type', 'text');
    expect(input).toHaveClass('flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background');
    expect(input).not.toBeDisabled();
  });

  it('applies custom className', () => {
    render(<Input className="custom-class" data-testid="input" />);
    const input = screen.getByTestId('input');
    
    expect(input).toHaveClass('custom-class');
  });

  it('renders with a placeholder', () => {
    render(<Input placeholder="Enter text" data-testid="input" />);
    const input = screen.getByPlaceholderText('Enter text');
    
    expect(input).toBeInTheDocument();
  });

  it('handles value and onChange', async () => {
    const handleChange = jest.fn();
    const user = userEvent.setup();
    
    render(<Input onChange={handleChange} data-testid="input" />);
    const input = screen.getByTestId('input');
    
    await user.type(input, 'Hello');
    
    expect(handleChange).toHaveBeenCalledTimes(5); // One call per character
    expect(input).toHaveValue('Hello');
  });

  it('can be disabled', () => {
    render(<Input disabled data-testid="input" />);
    const input = screen.getByTestId('input');
    
    expect(input).toBeDisabled();
    expect(input).toHaveClass('disabled:opacity-50');
  });

  it('renders with a custom type', () => {
    render(<Input type="password" data-testid="input" />);
    const input = screen.getByTestId('input');
    
    expect(input).toHaveAttribute('type', 'password');
  });

  it('forwards ref to the input element', () => {
    const ref = React.createRef<HTMLInputElement>();
    render(<Input ref={ref} data-testid="input" />);
    
    expect(ref.current).toBeInstanceOf(HTMLInputElement);
    expect(ref.current).toEqual(screen.getByTestId('input'));
  });

  it('applies focus styles when focused', () => {
    render(<Input data-testid="input" />);
    const input = screen.getByTestId('input');
    
    input.focus();
    
    // Check for focus-visible classes
    expect(input).toHaveClass('focus-visible:outline-none');
    expect(input).toHaveClass('focus-visible:ring-2');
    expect(input).toHaveClass('focus-visible:ring-ring');
    expect(input).toHaveClass('focus-visible:ring-offset-2');
  });

  it('renders with file type correctly', () => {
    render(<Input type="file" data-testid="input" />);
    const input = screen.getByTestId('input');
    
    expect(input).toHaveAttribute('type', 'file');
    expect(input).toHaveClass('file:border-0');
    expect(input).toHaveClass('file:bg-transparent');
    expect(input).toHaveClass('file:text-sm');
    expect(input).toHaveClass('file:font-medium');
  });

  it('renders with custom id and name attributes', () => {
    render(<Input id="username" name="username" data-testid="input" />);
    const input = screen.getByTestId('input');
    
    expect(input).toHaveAttribute('id', 'username');
    expect(input).toHaveAttribute('name', 'username');
  });
});
