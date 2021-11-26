package fr.utbm.vrp.agents;

import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Address;
import io.sarl.lang.core.Event;

/**
 * Event from VehicleAgent to AllocationAgent to tell that the customer has been inserted
 * <br>It is a reply to insertCustomer event
 */
@SarlSpecification("0.12")
@SarlElementType(15)
@SuppressWarnings("all")
public class customerInserted extends Event {
  @SyntheticMember
  public customerInserted() {
    super();
  }
  
  @SyntheticMember
  public customerInserted(final Address source) {
    super(source);
  }
  
  @SyntheticMember
  private static final long serialVersionUID = 588368462L;
}