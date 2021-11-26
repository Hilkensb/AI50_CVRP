package fr.utbm.vrp.agents;

import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Address;
import io.sarl.lang.core.Event;

/**
 * Event from VehicleAgent to AllocationAgent to tell that the customer have been inserted
 */
@SarlSpecification("0.12")
@SarlElementType(15)
@SuppressWarnings("all")
public class customerRelocated extends Event {
  @SyntheticMember
  public customerRelocated() {
    super();
  }
  
  @SyntheticMember
  public customerRelocated(final Address source) {
    super(source);
  }
  
  @SyntheticMember
  private static final long serialVersionUID = 588368462L;
}