<section>
  <h2>Python Financial Automation Sample</h2>
  <p>Sample Python logic for calculating Kenyan PAYE & statutory deductions:</p>
  
  <pre><code style="background-color: #f4f4f4; display: block; padding: 12px; border-radius: 4px; overflow-x: auto;">
def calculate_paye(gross_salary):
    # Tax Band Rates (Kenyan iTax Logic)
    if gross_salary <= 24000:
        tax = gross_salary * 0.10
    elif gross_salary <= 32333:
        tax = (24000 * 0.10) + ((gross_salary - 24000) * 0.25)
    else:
        tax = (24000 * 0.10) + (8333 * 0.25) + ((gross_salary - 32333) * 0.30)
    
    personal_relief = 2400
    net_paye = max(0, tax - personal_relief)
    return net_paye
  </code></pre>
  
  <p><a href="https://github.com/shadrackmakomere/shadrack-portfolio/tree/main/python-projects" target="_blank">View full script repository on GitHub &rarr;</a></p>
</section>
