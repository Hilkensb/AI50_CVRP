package fr.utbm.cvrp.solver;

import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Event;
import java.util.UUID;
import org.eclipse.xtext.xbase.lib.Pure;
import org.eclipse.xtext.xbase.lib.util.ToStringBuilder;

@SarlSpecification("0.12")
@SarlElementType(15)
@SuppressWarnings("all")
public class relocateCostEstimation extends Event {
  public final double cost;
  
  public relocateCostEstimation(final double cost_value, final UUID source_id_value) {
    this.cost = cost_value;
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
    relocateCostEstimation other = (relocateCostEstimation) obj;
    if (Double.doubleToLongBits(other.cost) != Double.doubleToLongBits(this.cost))
      return false;
    return super.equals(obj);
  }
  
  @Override
  @Pure
  @SyntheticMember
  public int hashCode() {
    int result = super.hashCode();
    final int prime = 31;
    result = prime * result + Double.hashCode(this.cost);
    return result;
  }
  
  /**
   * Returns a String representation of the relocateCostEstimation event's attributes only.
   */
  @SyntheticMember
  @Pure
  protected void toString(final ToStringBuilder builder) {
    super.toString(builder);
    builder.add("cost", this.cost);
  }
  
  @SyntheticMember
  private static final long serialVersionUID = -1621866377L;
}
