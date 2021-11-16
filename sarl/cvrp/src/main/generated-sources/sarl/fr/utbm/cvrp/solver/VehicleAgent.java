package fr.utbm.cvrp.solver;

import com.google.common.base.Objects;
import fr.utbm.cvrp.solver.customerInserted;
import fr.utbm.cvrp.solver.customerRelocated;
import fr.utbm.cvrp.solver.die;
import fr.utbm.cvrp.solver.finishVehicle;
import fr.utbm.cvrp.solver.insertCustomer;
import fr.utbm.cvrp.solver.insertCustomerEstimate;
import fr.utbm.cvrp.solver.insertionCostEstimation;
import fr.utbm.cvrp.solver.relocate;
import fr.utbm.cvrp.solver.relocateCostEstimation;
import fr.utbm.cvrp.solver.relocateCustomer;
import fr.utbm.cvrp.solver.relocateCustomerEstimate;
import fr.utbm.cvrp.solver.removeAll;
import fr.utbm.cvrp.solver.solution;
import io.sarl.core.DefaultContextInteractions;
import io.sarl.core.Destroy;
import io.sarl.core.Initialize;
import io.sarl.core.Lifecycle;
import io.sarl.core.Logging;
import io.sarl.lang.annotation.ImportedCapacityFeature;
import io.sarl.lang.annotation.PerceptGuardEvaluator;
import io.sarl.lang.annotation.SarlElementType;
import io.sarl.lang.annotation.SarlSpecification;
import io.sarl.lang.annotation.SyntheticMember;
import io.sarl.lang.core.Address;
import io.sarl.lang.core.Agent;
import io.sarl.lang.core.AtomicSkillReference;
import io.sarl.lang.core.DynamicSkillProvider;
import io.sarl.lang.core.Event;
import io.sarl.lang.core.Scope;
import io.sarl.lang.util.SerializableProxy;
import java.io.ObjectStreamException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import javax.inject.Inject;
import org.eclipse.xtext.xbase.lib.Conversions;
import org.eclipse.xtext.xbase.lib.Extension;
import org.eclipse.xtext.xbase.lib.Pure;

/**
 * VehicleAgent
 * <br>His goal is to keep a valid solution route
 */
@SarlSpecification("0.12")
@SarlElementType(19)
@SuppressWarnings("all")
public class VehicleAgent extends Agent {
  private String depot;
  
  private AtomicInteger vehicle_capacity = new AtomicInteger();
  
  private ArrayList<String> customers = new ArrayList<String>();
  
  private AtomicInteger demand_supplied = new AtomicInteger(0);
  
  private UUID allocationAgentUUID;
  
  private void $behaviorUnit$Initialize$0(final Initialize occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.setLoggingName("Vehicle Agent");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("The agent has started.");
    Object _get = occurrence.parameters[2];
    this.allocationAgentUUID = ((UUID) _get);
    Object _get_1 = occurrence.parameters[0];
    this.depot = (_get_1 == null ? null : _get_1.toString());
    Object _get_2 = occurrence.parameters[1];
    this.vehicle_capacity = ((AtomicInteger) _get_2);
    this.customers.add(this.depot);
    this.customers.add(this.depot);
  }
  
  private void $behaviorUnit$insertCustomerEstimate$1(final insertCustomerEstimate occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("New customer received.");
    double min_dist = Integer.MAX_VALUE;
    String customer_to_insert = occurrence.customer;
    int _get = this.demand_supplied.get();
    int _demand = this.getDemand(customer_to_insert);
    if (((_get + _demand) <= this.vehicle_capacity.doubleValue())) {
      for (int index = 0; (index < (((Object[])Conversions.unwrapArray(this.customers, Object.class)).length - 1)); index++) {
        {
          double insertion_cost = this.insertionCost(index, customer_to_insert);
          if ((insertion_cost < min_dist)) {
            min_dist = insertion_cost;
          }
        }
      }
    }
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    insertionCostEstimation _insertionCostEstimation = new insertionCostEstimation(min_dist);
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_insertionCostEstimation, _function);
  }
  
  private void $behaviorUnit$insertCustomer$2(final insertCustomer occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Inserting customer");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info(occurrence.customer);
    double min_dist = Integer.MAX_VALUE;
    String customer_to_insert = occurrence.customer;
    int best_index = 0;
    int _get = this.demand_supplied.get();
    int _demand = this.getDemand(customer_to_insert);
    if (((_get + _demand) <= this.vehicle_capacity.doubleValue())) {
      for (int index = 0; (index < (((Object[])Conversions.unwrapArray(this.customers, Object.class)).length - 1)); index++) {
        {
          double insertion_cost = this.insertionCost(index, customer_to_insert);
          if ((insertion_cost < min_dist)) {
            min_dist = insertion_cost;
            best_index = index;
          }
        }
      }
    }
    synchronized (this) {
      this.customers.add((best_index + 1), customer_to_insert);
    }
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info(this.customers.toString());
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    customerInserted _customerInserted = new customerInserted();
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_customerInserted, _function);
  }
  
  private void $behaviorUnit$finishVehicle$3(final finishVehicle occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Finish event received.");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info(this.customers.toString());
    solution solutionEvt = new solution(this.customers);
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(solutionEvt, _function);
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info("Solution sent.");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3.info("Killing myself.");
    Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.killMe();
  }
  
  private void $behaviorUnit$Destroy$4(final Destroy occurrence) {
    die dieEvt = new die();
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(dieEvt, _function);
  }
  
  private void $behaviorUnit$removeAll$5(final removeAll occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Removing all my customers");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info(this.customers.toString());
    ArrayList<String> customers_copy = new ArrayList<String>();
    for (int customer_index = 1; (customer_index < (((Object[])Conversions.unwrapArray(this.customers, Object.class)).length - 1)); customer_index++) {
      customers_copy.add(this.customers.get(customer_index));
    }
    this.customers.clear();
    this.customers.add(this.depot);
    this.customers.add(this.depot);
    this.demand_supplied.set(0);
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info(customers_copy);
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    relocate _relocate = new relocate(customers_copy);
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_relocate, _function);
  }
  
  private void $behaviorUnit$relocateCustomerEstimate$6(final relocateCustomerEstimate occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("New customer to relocate received.");
    double min_dist = Integer.MAX_VALUE;
    String customer_to_insert = occurrence.customer;
    int _get = this.demand_supplied.get();
    int _demand = this.getDemand(customer_to_insert);
    if (((_get + _demand) <= this.vehicle_capacity.doubleValue())) {
      for (int index = 0; (index < (((Object[])Conversions.unwrapArray(this.customers, Object.class)).length - 1)); index++) {
        {
          double insertion_cost = this.insertionCost(index, customer_to_insert);
          if ((insertion_cost < min_dist)) {
            min_dist = insertion_cost;
          }
        }
      }
    }
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    UUID _iD = this.getID();
    relocateCostEstimation _relocateCostEstimation = new relocateCostEstimation(min_dist, _iD);
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_relocateCostEstimation, _function);
  }
  
  private void $behaviorUnit$relocateCustomer$7(final relocateCustomer occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Relocating customer");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info(occurrence.customer);
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info(this.customers.toString());
    double min_dist = Integer.MAX_VALUE;
    String customer_to_insert = occurrence.customer;
    int best_index = 0;
    int _get = this.demand_supplied.get();
    int _demand = this.getDemand(customer_to_insert);
    if (((_get + _demand) <= this.vehicle_capacity.doubleValue())) {
      for (int index = 0; (index < (((Object[])Conversions.unwrapArray(this.customers, Object.class)).length - 1)); index++) {
        {
          double insertion_cost = this.insertionCost(index, customer_to_insert);
          if ((insertion_cost < min_dist)) {
            min_dist = insertion_cost;
            best_index = index;
          }
        }
      }
    }
    int _get_1 = this.demand_supplied.get();
    int _demand_1 = this.getDemand(customer_to_insert);
    int new_demand = (_get_1 + _demand_1);
    this.demand_supplied.set(new_demand);
    synchronized (this) {
      this.customers.add((best_index + 1), customer_to_insert);
    }
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3.info(this.customers.toString());
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    customerRelocated _customerRelocated = new customerRelocated();
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_allocationAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_allocationAgentUUID_1) {
        this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_allocationAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, VehicleAgent.this.allocationAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, VehicleAgent.this.allocationAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_customerRelocated, _function);
  }
  
  /**
   * TaskAgent methods behavior
   */
  @Pure
  protected int getId(final String customer_string) {
    String customer_id_string = customer_string.split(" ")[0];
    int customer_id = Integer.parseInt(customer_id_string);
    return customer_id;
  }
  
  @Pure
  protected int getX(final String customer_string) {
    String customer_x_string = customer_string.split(" ")[1];
    int customer_x = Integer.parseInt(customer_x_string);
    return customer_x;
  }
  
  @Pure
  protected int getY(final String customer_string) {
    String customer_y_string = customer_string.split(" ")[2];
    int customer_y = Integer.parseInt(customer_y_string);
    return customer_y;
  }
  
  @Pure
  protected int getDemand(final String customer_string) {
    String customer_demand_string = customer_string.split(" ")[3];
    int customer_demand = Integer.parseInt(customer_demand_string);
    return customer_demand;
  }
  
  @Pure
  protected double getDistance(final int x1, final int x2, final int y1, final int y2) {
    double _pow = Math.pow((x1 - x2), 2.0);
    double _pow_1 = Math.pow((y1 - y2), 2.0);
    return Math.sqrt((_pow + _pow_1));
  }
  
  @Pure
  protected double insertionCost(final int index, final String customer) {
    synchronized (this) {
      double distance_1 = this.getDistance(this.getX(this.customers.get(index)), this.getX(this.customers.get((index + 1))), 
        this.getY(this.customers.get(index)), this.getY(this.customers.get((index + 1))));
      double distance_2 = this.getDistance(this.getX(customer), this.getX(this.customers.get((index + 1))), this.getY(customer), 
        this.getY(this.customers.get((index + 1))));
      double distance_3 = this.getDistance(this.getX(this.customers.get(index)), this.getY(customer), 
        this.getY(this.customers.get(index)), this.getY(customer));
      return ((distance_1 + distance_2) - distance_3);
    }
  }
  
  @Extension
  @ImportedCapacityFeature(Logging.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_LOGGING;
  
  @SyntheticMember
  @Pure
  private Logging $CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_LOGGING == null || this.$CAPACITY_USE$IO_SARL_CORE_LOGGING.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_LOGGING = $getSkill(Logging.class);
    }
    return $castSkill(Logging.class, this.$CAPACITY_USE$IO_SARL_CORE_LOGGING);
  }
  
  @Extension
  @ImportedCapacityFeature(DefaultContextInteractions.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS;
  
  @SyntheticMember
  @Pure
  private DefaultContextInteractions $CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS == null || this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS = $getSkill(DefaultContextInteractions.class);
    }
    return $castSkill(DefaultContextInteractions.class, this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS);
  }
  
  @Extension
  @ImportedCapacityFeature(Lifecycle.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_LIFECYCLE;
  
  @SyntheticMember
  @Pure
  private Lifecycle $CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE == null || this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE = $getSkill(Lifecycle.class);
    }
    return $castSkill(Lifecycle.class, this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE);
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$Initialize(final Initialize occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$Initialize$0(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$insertCustomerEstimate(final insertCustomerEstimate occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$insertCustomerEstimate$1(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$insertCustomer(final insertCustomer occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$insertCustomer$2(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$Destroy(final Destroy occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$Destroy$4(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$removeAll(final removeAll occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$removeAll$5(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$relocateCustomerEstimate(final relocateCustomerEstimate occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$relocateCustomerEstimate$6(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$relocateCustomer(final relocateCustomer occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$relocateCustomer$7(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$finishVehicle(final finishVehicle occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$finishVehicle$3(occurrence));
  }
  
  @SyntheticMember
  @Override
  public void $getSupportedEvents(final Set<Class<? extends Event>> toBeFilled) {
    super.$getSupportedEvents(toBeFilled);
    toBeFilled.add(finishVehicle.class);
    toBeFilled.add(insertCustomer.class);
    toBeFilled.add(insertCustomerEstimate.class);
    toBeFilled.add(relocateCustomer.class);
    toBeFilled.add(relocateCustomerEstimate.class);
    toBeFilled.add(removeAll.class);
    toBeFilled.add(Destroy.class);
    toBeFilled.add(Initialize.class);
  }
  
  @SyntheticMember
  @Override
  public boolean $isSupportedEvent(final Class<? extends Event> event) {
    if (finishVehicle.class.isAssignableFrom(event)) {
      return true;
    }
    if (insertCustomer.class.isAssignableFrom(event)) {
      return true;
    }
    if (insertCustomerEstimate.class.isAssignableFrom(event)) {
      return true;
    }
    if (relocateCustomer.class.isAssignableFrom(event)) {
      return true;
    }
    if (relocateCustomerEstimate.class.isAssignableFrom(event)) {
      return true;
    }
    if (removeAll.class.isAssignableFrom(event)) {
      return true;
    }
    if (Destroy.class.isAssignableFrom(event)) {
      return true;
    }
    if (Initialize.class.isAssignableFrom(event)) {
      return true;
    }
    return false;
  }
  
  @SyntheticMember
  @Override
  public void $evaluateBehaviorGuards(final Object event, final Collection<Runnable> callbacks) {
    super.$evaluateBehaviorGuards(event, callbacks);
    if (event instanceof finishVehicle) {
      final finishVehicle occurrence = (finishVehicle) event;
      $guardEvaluator$finishVehicle(occurrence, callbacks);
    }
    if (event instanceof insertCustomer) {
      final insertCustomer occurrence = (insertCustomer) event;
      $guardEvaluator$insertCustomer(occurrence, callbacks);
    }
    if (event instanceof insertCustomerEstimate) {
      final insertCustomerEstimate occurrence = (insertCustomerEstimate) event;
      $guardEvaluator$insertCustomerEstimate(occurrence, callbacks);
    }
    if (event instanceof relocateCustomer) {
      final relocateCustomer occurrence = (relocateCustomer) event;
      $guardEvaluator$relocateCustomer(occurrence, callbacks);
    }
    if (event instanceof relocateCustomerEstimate) {
      final relocateCustomerEstimate occurrence = (relocateCustomerEstimate) event;
      $guardEvaluator$relocateCustomerEstimate(occurrence, callbacks);
    }
    if (event instanceof removeAll) {
      final removeAll occurrence = (removeAll) event;
      $guardEvaluator$removeAll(occurrence, callbacks);
    }
    if (event instanceof Destroy) {
      final Destroy occurrence = (Destroy) event;
      $guardEvaluator$Destroy(occurrence, callbacks);
    }
    if (event instanceof Initialize) {
      final Initialize occurrence = (Initialize) event;
      $guardEvaluator$Initialize(occurrence, callbacks);
    }
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
    VehicleAgent other = (VehicleAgent) obj;
    if (!java.util.Objects.equals(this.depot, other.depot))
      return false;
    if (!java.util.Objects.equals(this.allocationAgentUUID, other.allocationAgentUUID))
      return false;
    return super.equals(obj);
  }
  
  @Override
  @Pure
  @SyntheticMember
  public int hashCode() {
    int result = super.hashCode();
    final int prime = 31;
    result = prime * result + java.util.Objects.hashCode(this.depot);
    result = prime * result + java.util.Objects.hashCode(this.allocationAgentUUID);
    return result;
  }
  
  @SyntheticMember
  public VehicleAgent(final UUID parentID, final UUID agentID) {
    super(parentID, agentID);
  }
  
  @SyntheticMember
  @Inject
  public VehicleAgent(final UUID parentID, final UUID agentID, final DynamicSkillProvider skillProvider) {
    super(parentID, agentID, skillProvider);
  }
}
