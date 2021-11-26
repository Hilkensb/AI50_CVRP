package fr.utbm.vrp.agents;

import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Event;
import java.util.Objects;
import org.eclipse.xtext.xbase.lib.Pure;
import org.eclipse.xtext.xbase.lib.util.ToStringBuilder;

/**
 * Event from AllocationAgent to VehicleAgent to tell the vehicle to insert the given
 * customer
 * <br>It's launched when all vehicle agents have send their insertion cost estimation
 * through insertionCostEstimation event
 * 
 * @param customer The customer to insert
 */
@SarlSpecification("0.12")
@SarlElementType(15)
@SuppressWarnings("all")
public class insertCustomer extends Event {
  public final String customer;
  
  public insertCustomer(final String customer_value) {
    this.customer = customer_value;
  }
  
  @Override
  @Pure
  @SyntheticMember
  public boolean equals(final Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    insertCustomer other = (insertCustomer) obj;
    if (!Objects.equals(this.customer, other.customer))
      return false;
    return super.equals(obj);
  }
  
  @Override
  @Pure
  @SyntheticMember
  public int hashCode() {
    int result = super.hashCode();
    final int prime = 31;
    result = prime * result + Objects.hashCode(this.customer);
    return result;
  }
  
  /**
   * Returns a String representation of the insertCustomer event's attributes only.
   */
  @SyntheticMember
  @Pure
  protected void toString(final ToStringBuilder builder) {
    super.toString(builder);
    builder.add("customer", this.customer);
  }
  
  @SyntheticMember
  private static final long serialVersionUID = 788144931L;
}