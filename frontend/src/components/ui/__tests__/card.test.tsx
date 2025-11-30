import React from 'react';
import { render, screen } from '@testing-library/react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../card';

describe('Card', () => {
  it('renders a basic card with content', () => {
    render(
      <Card data-testid="card">
        <CardContent>Card Content</CardContent>
      </Card>
    );
    
    const card = screen.getByTestId('card');
    const content = screen.getByText('Card Content');
    
    expect(card).toBeInTheDocument();
    expect(card).toHaveClass('rounded-lg', 'border', 'bg-card', 'text-card-foreground', 'shadow-sm');
    expect(content).toBeInTheDocument();
  });

  it('renders a card with header and title', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
        </CardHeader>
        <CardContent>Card Content</CardContent>
      </Card>
    );
    
    const title = screen.getByText('Card Title');
    const content = screen.getByText('Card Content');
    
    expect(title).toBeInTheDocument();
    expect(title).toHaveClass('text-2xl', 'font-semibold', 'leading-none', 'tracking-tight');
    expect(content).toBeInTheDocument();
  });

  it('renders a card with description', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>This is a description</CardDescription>
        </CardHeader>
        <CardContent>Card Content</CardContent>
      </Card>
    );
    
    const description = screen.getByText('This is a description');
    
    expect(description).toBeInTheDocument();
    expect(description).toHaveClass('text-sm', 'text-muted-foreground');
  });

  it('renders a card with footer', () => {
    render(
      <Card>
        <CardContent>Card Content</CardContent>
        <CardFooter>Card Footer</CardFooter>
      </Card>
    );
    
    const footer = screen.getByText('Card Footer');
    
    expect(footer).toBeInTheDocument();
    expect(footer).toHaveClass('flex', 'items-center', 'p-6', 'pt-0');
  });

  it('applies custom className to card', () => {
    render(
      <Card className="custom-card-class" data-testid="card">
        <CardContent>Card Content</CardContent>
      </Card>
    );
    
    const card = screen.getByTestId('card');
    
    expect(card).toHaveClass('custom-card-class');
  });

  it('applies custom className to card header', () => {
    render(
      <Card>
        <CardHeader className="custom-header-class">
          <CardTitle>Card Title</CardTitle>
        </CardHeader>
        <CardContent>Card Content</CardContent>
      </Card>
    );
    
    const header = screen.getByText('Card Title').closest('div');
    
    expect(header).toHaveClass('custom-header-class');
  });

  it('applies custom className to card content', () => {
    render(
      <Card>
        <CardContent className="custom-content-class">Card Content</CardContent>
      </Card>
    );
    
    const content = screen.getByText('Card Content');
    
    expect(content).toHaveClass('custom-content-class');
    expect(content).toHaveClass('p-6', 'pt-0');
  });

  it('applies custom className to card footer', () => {
    render(
      <Card>
        <CardContent>Card Content</CardContent>
        <CardFooter className="custom-footer-class">Card Footer</CardFooter>
      </Card>
    );
    
    const footer = screen.getByText('Card Footer');
    
    expect(footer).toHaveClass('custom-footer-class');
  });

  it('renders card with all parts', () => {
    render(
      <Card data-testid="card">
        <CardHeader data-testid="header">
          <CardTitle data-testid="title">Card Title</CardTitle>
          <CardDescription data-testid="description">Card Description</CardDescription>
        </CardHeader>
        <CardContent data-testid="content">Card Content</CardContent>
        <CardFooter data-testid="footer">Card Footer</CardFooter>
      </Card>
    );
    
    const card = screen.getByTestId('card');
    const header = screen.getByTestId('header');
    const title = screen.getByTestId('title');
    const description = screen.getByTestId('description');
    const content = screen.getByTestId('content');
    const footer = screen.getByTestId('footer');
    
    expect(card).toContainElement(header);
    expect(header).toContainElement(title);
    expect(header).toContainElement(description);
    expect(card).toContainElement(content);
    expect(card).toContainElement(footer);
  });
});
