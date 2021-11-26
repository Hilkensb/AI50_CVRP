package fr.utbm.vrp.agents;

import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Address;
import io.sarl.lang.core.Event;

/**
 * Event from AllocationAgent to VehicleAgent to indicates that there is no
 * more customer to insert
 */
@SarlSpecification("0.12")
@SarlElementType(15)
@SuppressWarnings("all")
public class finishVehicle extends Event {
  @SyntheticMember
  public finishVehicle() {
    super();
  }
  
  @SyntheticMember
  public finishVehicle(final Address source) {
    super(source);
  }
  
  @SyntheticMember
  private static final long serialVersionUID = 588368462L;
}
