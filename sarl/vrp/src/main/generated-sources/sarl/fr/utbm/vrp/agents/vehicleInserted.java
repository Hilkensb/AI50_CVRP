package fr.utbm.vrp.agents;

import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Address;
import io.sarl.lang.core.Event;

/**
 * Event triggered by AllocationAgent to TaskAgent to prevent that
 * a new vehicle has been inserted
 */
@SarlSpecification("0.12")
@SarlElementType(15)
@SuppressWarnings("all")
public class vehicleInserted extends Event {
  @SyntheticMember
  public vehicleInserted() {
    super();
  }
  
  @SyntheticMember
  public vehicleInserted(final Address source) {
    super(source);
  }
  
  @SyntheticMember
  private static final long serialVersionUID = 588368462L;
}
