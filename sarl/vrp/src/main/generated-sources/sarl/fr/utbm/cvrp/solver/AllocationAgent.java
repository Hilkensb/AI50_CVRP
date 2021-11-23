package fr.utbm.cvrp.solver;

import com.google.common.base.Objects;
import fr.utbm.cvrp.solver.VehicleAgent;
import fr.utbm.cvrp.solver.customerInserted;
import fr.utbm.cvrp.solver.customerRelocated;
import fr.utbm.cvrp.solver.finish;
import fr.utbm.cvrp.solver.finishVehicle;
import fr.utbm.cvrp.solver.insertCustomer;
import fr.utbm.cvrp.solver.insertCustomerEstimate;
import fr.utbm.cvrp.solver.insertionCostEstimation;
import fr.utbm.cvrp.solver.nextCustomer;
import fr.utbm.cvrp.solver.nextCustomerRequest;
import fr.utbm.cvrp.solver.relocate;
import fr.utbm.cvrp.solver.relocateCostEstimation;
import fr.utbm.cvrp.solver.relocateCustomer;
import fr.utbm.cvrp.solver.relocateCustomerEstimate;
import fr.utbm.cvrp.solver.removeAll;
import fr.utbm.cvrp.solver.solution;
import io.sarl.core.AgentTask;
import io.sarl.core.DefaultContextInteractions;
import io.sarl.core.Initialize;
import io.sarl.core.InnerContextAccess;
import io.sarl.core.Lifecycle;
import io.sarl.core.Logging;
import io.sarl.core.MemberLeft;
import io.sarl.core.Schedules;
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
import io.sarl.lang.util.ConcurrentSet;
import io.sarl.lang.util.SerializableProxy;
import java.io.ObjectStreamException;
import java.util.Collection;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicInteger;
import javax.inject.Inject;
import org.eclipse.xtext.xbase.lib.Extension;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.eclipse.xtext.xbase.lib.Pure;

/**
 * AllocationAgent
 * <br>His goal is to insert customers where the insertion cost is minimized
 * <br>Strategies: CNP-RA
 */
@SarlSpecification("0.12")
@SarlElementType(19)
@SuppressWarnings("all")
public class AllocationAgent extends Agent {
  private String depot;
  
  private AtomicInteger vehicle_capacity = new AtomicInteger();
  
  private UUID taskAgentUUID;
  
  private AtomicInteger number_vehicle;
  
  private String actual_customer_insert;
  
  private int number_agent_returned = 0;
  
  private double best_insertion_cost = Double.MAX_VALUE;
  
  private UUID best_vehicle_insert;
  
  private ConcurrentLinkedQueue<UUID> vehicle_agents = new ConcurrentLinkedQueue<UUID>();
  
  private ConcurrentLinkedQueue<String> customer_relocate = new ConcurrentLinkedQueue<String>();
  
  private void $behaviorUnit$Initialize$0(final Initialize occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.setLoggingName("Allocation Agent");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("The agent has started.");
    Object _get = occurrence.parameters[0];
    this.depot = (_get == null ? null : _get.toString());
    Object _get_1 = occurrence.parameters[1];
    this.vehicle_capacity = ((AtomicInteger) _get_1);
    Object _get_2 = occurrence.parameters[2];
    Integer number_vehicle_int = ((Integer) _get_2);
    AtomicInteger _atomicInteger = new AtomicInteger(((number_vehicle_int) == null ? 0 : (number_vehicle_int).intValue()));
    this.number_vehicle = _atomicInteger;
    Object _get_3 = occurrence.parameters[3];
    this.taskAgentUUID = ((UUID) _get_3);
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info(occurrence.getSource().getID());
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3.info(this.taskAgentUUID);
    for (int vehicle_i = 1; (vehicle_i <= number_vehicle_int.doubleValue()); vehicle_i++) {
      {
        UUID vehicleUUID = UUID.randomUUID();
        Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
        InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.spawnInContextWithID(VehicleAgent.class, vehicleUUID, _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext(), this.depot, this.vehicle_capacity, this.getID());
      }
    }
    Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
    final AgentTask task = _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER.task("waiting_for_vehicle_agent");
    Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
    final Procedure1<Agent> _function = (Agent it) -> {
      InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
      int _memberAgentCount = _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getMemberAgentCount();
      int _get_4 = this.number_vehicle.get();
      if ((_memberAgentCount == _get_4)) {
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_4 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_4.info("New customer is requested.");
        DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
        nextCustomerRequest _nextCustomerRequest = new nextCustomerRequest();
        class $SerializableClosureProxy implements Scope<Address> {
          
          private final UUID $_taskAgentUUID_1;
          
          public $SerializableClosureProxy(final UUID $_taskAgentUUID_1) {
            this.$_taskAgentUUID_1 = $_taskAgentUUID_1;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, $_taskAgentUUID_1);
          }
        }
        final Scope<Address> _function_1 = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, AllocationAgent.this.taskAgentUUID);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy.class, AllocationAgent.this.taskAgentUUID);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_nextCustomerRequest, _function_1);
        Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_2.cancel(task);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_1.every(task, 100, _function);
  }
  
  private void $behaviorUnit$nextCustomer$1(final nextCustomer occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("New customer received.");
    this.actual_customer_insert = occurrence.customer;
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    insertCustomerEstimate _insertCustomerEstimate = new insertCustomerEstimate(this.actual_customer_insert);
    _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), _insertCustomerEstimate, null);
  }
  
  private void $behaviorUnit$finish$2(final finish occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Emitting finish event.");
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    finishVehicle _finishVehicle = new finishVehicle();
    _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), _finishVehicle, null);
  }
  
  private void $behaviorUnit$MemberLeft$3(final MemberLeft occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("A VehicleAgent has die.");
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    int _memberAgentCount = _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getMemberAgentCount();
    if ((_memberAgentCount == 0)) {
      Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("Killing myself.");
      Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.killMe();
    }
  }
  
  private void $behaviorUnit$solution$4(final solution occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Solution received.");
    DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
    solution _solution = new solution(occurrence.route);
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID $_taskAgentUUID_1;
      
      public $SerializableClosureProxy(final UUID $_taskAgentUUID_1) {
        this.$_taskAgentUUID_1 = $_taskAgentUUID_1;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, $_taskAgentUUID_1);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, AllocationAgent.this.taskAgentUUID);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, AllocationAgent.this.taskAgentUUID);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_solution, _function);
  }
  
  private void $behaviorUnit$customerInserted$5(final customerInserted occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Customer inserted.");
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    ConcurrentSet<UUID> _memberAgents = _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getMemberAgents();
    for (final UUID vehicle_agent : _memberAgents) {
      this.vehicle_agents.add(vehicle_agent);
    }
    UUID vehicle_customer_relocate = this.vehicle_agents.poll();
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    removeAll _removeAll = new removeAll();
    class $SerializableClosureProxy implements Scope<Address> {
      
      private final UUID vehicle_customer_relocate;
      
      public $SerializableClosureProxy(final UUID vehicle_customer_relocate) {
        this.vehicle_customer_relocate = vehicle_customer_relocate;
      }
      
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, vehicle_customer_relocate);
      }
    }
    final Scope<Address> _function = new Scope<Address>() {
      @Override
      public boolean matches(final Address it) {
        UUID _iD = it.getID();
        return Objects.equal(_iD, vehicle_customer_relocate);
      }
      private Object writeReplace() throws ObjectStreamException {
        return new SerializableProxy($SerializableClosureProxy.class, vehicle_customer_relocate);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1.getInnerContext().getDefaultSpace().emit(this.getID(), _removeAll, _function);
  }
  
  private void $behaviorUnit$relocate$6(final relocate occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Relocating all customers.");
    boolean _isEmpty = occurrence.customers.isEmpty();
    if (_isEmpty) {
      Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
      _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("Empty vehicle.");
      boolean _isEmpty_1 = this.vehicle_agents.isEmpty();
      if ((!_isEmpty_1)) {
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info("Go for the next VehicleAgent.");
        UUID vehicle_customer_relocate = this.vehicle_agents.poll();
        InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
        removeAll _removeAll = new removeAll();
        class $SerializableClosureProxy implements Scope<Address> {
          
          private final UUID vehicle_customer_relocate;
          
          public $SerializableClosureProxy(final UUID vehicle_customer_relocate) {
            this.vehicle_customer_relocate = vehicle_customer_relocate;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, vehicle_customer_relocate);
          }
        }
        final Scope<Address> _function = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, vehicle_customer_relocate);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy.class, vehicle_customer_relocate);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), _removeAll, _function);
      } else {
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3.info("No more VehicleAgent to relocate customers");
        DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
        nextCustomerRequest _nextCustomerRequest = new nextCustomerRequest();
        class $SerializableClosureProxy_1 implements Scope<Address> {
          
          private final UUID $_taskAgentUUID_1;
          
          public $SerializableClosureProxy_1(final UUID $_taskAgentUUID_1) {
            this.$_taskAgentUUID_1 = $_taskAgentUUID_1;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, $_taskAgentUUID_1);
          }
        }
        final Scope<Address> _function_1 = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, AllocationAgent.this.taskAgentUUID);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy_1.class, AllocationAgent.this.taskAgentUUID);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_nextCustomerRequest, _function_1);
      }
    } else {
      for (final String customer : occurrence.customers) {
        this.customer_relocate.add(customer);
      }
      this.actual_customer_insert = this.customer_relocate.poll();
      InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
      relocateCustomerEstimate _relocateCustomerEstimate = new relocateCustomerEstimate(this.actual_customer_insert);
      _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1.getInnerContext().getDefaultSpace().emit(this.getID(), _relocateCustomerEstimate, null);
    }
  }
  
  private void $behaviorUnit$customerRelocated$7(final customerRelocated occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Customer relocated.");
    boolean _isEmpty = this.customer_relocate.isEmpty();
    if (_isEmpty) {
      boolean _isEmpty_1 = this.vehicle_agents.isEmpty();
      if ((!_isEmpty_1)) {
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("Go for the next VehicleAgent.");
        UUID vehicle_customer_relocate = this.vehicle_agents.poll();
        InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
        removeAll _removeAll = new removeAll();
        class $SerializableClosureProxy implements Scope<Address> {
          
          private final UUID vehicle_customer_relocate;
          
          public $SerializableClosureProxy(final UUID vehicle_customer_relocate) {
            this.vehicle_customer_relocate = vehicle_customer_relocate;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, vehicle_customer_relocate);
          }
        }
        final Scope<Address> _function = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, vehicle_customer_relocate);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy.class, vehicle_customer_relocate);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), _removeAll, _function);
      } else {
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info("No more VehicleAgent to relocate customers");
        DefaultContextInteractions _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER();
        nextCustomerRequest _nextCustomerRequest = new nextCustomerRequest();
        class $SerializableClosureProxy_1 implements Scope<Address> {
          
          private final UUID $_taskAgentUUID_1;
          
          public $SerializableClosureProxy_1(final UUID $_taskAgentUUID_1) {
            this.$_taskAgentUUID_1 = $_taskAgentUUID_1;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, $_taskAgentUUID_1);
          }
        }
        final Scope<Address> _function_1 = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, AllocationAgent.this.taskAgentUUID);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy_1.class, AllocationAgent.this.taskAgentUUID);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_DEFAULTCONTEXTINTERACTIONS$CALLER.emit(_nextCustomerRequest, _function_1);
      }
    } else {
      this.actual_customer_insert = this.customer_relocate.poll();
      InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
      relocateCustomerEstimate _relocateCustomerEstimate = new relocateCustomerEstimate(this.actual_customer_insert);
      _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1.getInnerContext().getDefaultSpace().emit(this.getID(), _relocateCustomerEstimate, null);
    }
  }
  
  private void $behaviorUnit$relocateCostEstimation$8(final relocateCostEstimation occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Estimation received.");
    synchronized (this) {
      this.number_agent_returned++;
      if ((this.best_insertion_cost > occurrence.cost)) {
        this.best_insertion_cost = occurrence.cost;
        this.best_vehicle_insert = occurrence.getSource().getID();
      }
      if ((this.number_vehicle != null && this.number_agent_returned == this.number_vehicle.doubleValue())) {
        this.best_insertion_cost = Integer.MAX_VALUE;
        this.number_agent_returned = 0;
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("Request to relocate customer.");
        InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
        relocateCustomer _relocateCustomer = new relocateCustomer(this.actual_customer_insert);
        class $SerializableClosureProxy implements Scope<Address> {
          
          private final UUID $_best_vehicle_insert;
          
          public $SerializableClosureProxy(final UUID $_best_vehicle_insert) {
            this.$_best_vehicle_insert = $_best_vehicle_insert;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, $_best_vehicle_insert);
          }
        }
        final Scope<Address> _function = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, AllocationAgent.this.best_vehicle_insert);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy.class, AllocationAgent.this.best_vehicle_insert);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), _relocateCustomer, _function);
      }
    }
  }
  
  private void $behaviorUnit$insertionCostEstimation$9(final insertionCostEstimation occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Estimation received.");
    synchronized (this) {
      this.number_agent_returned++;
      if ((this.best_insertion_cost > occurrence.cost)) {
        this.best_insertion_cost = occurrence.cost;
        this.best_vehicle_insert = occurrence.getSource().getID();
      }
      if (((this.number_vehicle != null && this.number_agent_returned == this.number_vehicle.doubleValue()) && (this.best_insertion_cost < Integer.MAX_VALUE))) {
        this.best_insertion_cost = Integer.MAX_VALUE;
        this.number_agent_returned = 0;
        Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("Request to insert customer.");
        insertCustomer insertCustomerEvt = new insertCustomer(this.actual_customer_insert);
        InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
        class $SerializableClosureProxy implements Scope<Address> {
          
          private final UUID $_best_vehicle_insert;
          
          public $SerializableClosureProxy(final UUID $_best_vehicle_insert) {
            this.$_best_vehicle_insert = $_best_vehicle_insert;
          }
          
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, $_best_vehicle_insert);
          }
        }
        final Scope<Address> _function = new Scope<Address>() {
          @Override
          public boolean matches(final Address it) {
            UUID _iD = it.getID();
            return Objects.equal(_iD, AllocationAgent.this.best_vehicle_insert);
          }
          private Object writeReplace() throws ObjectStreamException {
            return new SerializableProxy($SerializableClosureProxy.class, AllocationAgent.this.best_vehicle_insert);
          }
        };
        _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), insertCustomerEvt, _function);
      } else {
        if ((this.number_vehicle != null && this.number_agent_returned == this.number_vehicle.doubleValue())) {
          Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
          _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info("Spawning a new vehicle agent.");
          this.best_insertion_cost = Integer.MAX_VALUE;
          this.number_agent_returned = 0;
          UUID vehicleUUID = UUID.randomUUID();
          Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
          InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
          _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.spawnInContextWithID(VehicleAgent.class, vehicleUUID, _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1.getInnerContext(), this.depot, this.vehicle_capacity, this.getID());
          this.number_vehicle.incrementAndGet();
          Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
          String _string = Integer.valueOf(this.number_vehicle.get()).toString();
          final AgentTask task = _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER.task(("waiting_for_vehicle_agent_" + _string));
          Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
          final Procedure1<Agent> _function_1 = (Agent it) -> {
            InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
            int _memberAgentCount = _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_2.getMemberAgentCount();
            int _get = this.number_vehicle.get();
            if ((_memberAgentCount == _get)) {
              Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
              _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_3.info("Restarting CNP.");
              InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_3 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
              insertCustomerEstimate _insertCustomerEstimate = new insertCustomerEstimate(this.actual_customer_insert);
              _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_3.getInnerContext().getDefaultSpace().emit(this.getID(), _insertCustomerEstimate, null);
              Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
              _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_2.cancel(task);
            }
          };
          _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_1.every(task, 100, _function_1);
        }
      }
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
  
  @Extension
  @ImportedCapacityFeature(InnerContextAccess.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS;
  
  @SyntheticMember
  @Pure
  private InnerContextAccess $CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS == null || this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS = $getSkill(InnerContextAccess.class);
    }
    return $castSkill(InnerContextAccess.class, this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS);
  }
  
  @Extension
  @ImportedCapacityFeature(Schedules.class)
  @SyntheticMember
  private transient AtomicSkillReference $CAPACITY_USE$IO_SARL_CORE_SCHEDULES;
  
  @SyntheticMember
  @Pure
  private Schedules $CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER() {
    if (this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES == null || this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES.get() == null) {
      this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES = $getSkill(Schedules.class);
    }
    return $castSkill(Schedules.class, this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES);
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
  private void $guardEvaluator$solution(final solution occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$solution$4(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$finish(final finish occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$finish$2(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$customerRelocated(final customerRelocated occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$customerRelocated$7(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$relocateCostEstimation(final relocateCostEstimation occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$relocateCostEstimation$8(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$nextCustomer(final nextCustomer occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$nextCustomer$1(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$MemberLeft(final MemberLeft occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$MemberLeft$3(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$relocate(final relocate occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$relocate$6(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$insertionCostEstimation(final insertionCostEstimation occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$insertionCostEstimation$9(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$customerInserted(final customerInserted occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$customerInserted$5(occurrence));
  }
  
  @SyntheticMember
  @Override
  public void $getSupportedEvents(final Set<Class<? extends Event>> toBeFilled) {
    super.$getSupportedEvents(toBeFilled);
    toBeFilled.add(customerInserted.class);
    toBeFilled.add(customerRelocated.class);
    toBeFilled.add(finish.class);
    toBeFilled.add(insertionCostEstimation.class);
    toBeFilled.add(nextCustomer.class);
    toBeFilled.add(relocate.class);
    toBeFilled.add(relocateCostEstimation.class);
    toBeFilled.add(solution.class);
    toBeFilled.add(Initialize.class);
    toBeFilled.add(MemberLeft.class);
  }
  
  @SyntheticMember
  @Override
  public boolean $isSupportedEvent(final Class<? extends Event> event) {
    if (customerInserted.class.isAssignableFrom(event)) {
      return true;
    }
    if (customerRelocated.class.isAssignableFrom(event)) {
      return true;
    }
    if (finish.class.isAssignableFrom(event)) {
      return true;
    }
    if (insertionCostEstimation.class.isAssignableFrom(event)) {
      return true;
    }
    if (nextCustomer.class.isAssignableFrom(event)) {
      return true;
    }
    if (relocate.class.isAssignableFrom(event)) {
      return true;
    }
    if (relocateCostEstimation.class.isAssignableFrom(event)) {
      return true;
    }
    if (solution.class.isAssignableFrom(event)) {
      return true;
    }
    if (Initialize.class.isAssignableFrom(event)) {
      return true;
    }
    if (MemberLeft.class.isAssignableFrom(event)) {
      return true;
    }
    return false;
  }
  
  @SyntheticMember
  @Override
  public void $evaluateBehaviorGuards(final Object event, final Collection<Runnable> callbacks) {
    super.$evaluateBehaviorGuards(event, callbacks);
    if (event instanceof customerInserted) {
      final customerInserted occurrence = (customerInserted) event;
      $guardEvaluator$customerInserted(occurrence, callbacks);
    }
    if (event instanceof customerRelocated) {
      final customerRelocated occurrence = (customerRelocated) event;
      $guardEvaluator$customerRelocated(occurrence, callbacks);
    }
    if (event instanceof finish) {
      final finish occurrence = (finish) event;
      $guardEvaluator$finish(occurrence, callbacks);
    }
    if (event instanceof insertionCostEstimation) {
      final insertionCostEstimation occurrence = (insertionCostEstimation) event;
      $guardEvaluator$insertionCostEstimation(occurrence, callbacks);
    }
    if (event instanceof nextCustomer) {
      final nextCustomer occurrence = (nextCustomer) event;
      $guardEvaluator$nextCustomer(occurrence, callbacks);
    }
    if (event instanceof relocate) {
      final relocate occurrence = (relocate) event;
      $guardEvaluator$relocate(occurrence, callbacks);
    }
    if (event instanceof relocateCostEstimation) {
      final relocateCostEstimation occurrence = (relocateCostEstimation) event;
      $guardEvaluator$relocateCostEstimation(occurrence, callbacks);
    }
    if (event instanceof solution) {
      final solution occurrence = (solution) event;
      $guardEvaluator$solution(occurrence, callbacks);
    }
    if (event instanceof Initialize) {
      final Initialize occurrence = (Initialize) event;
      $guardEvaluator$Initialize(occurrence, callbacks);
    }
    if (event instanceof MemberLeft) {
      final MemberLeft occurrence = (MemberLeft) event;
      $guardEvaluator$MemberLeft(occurrence, callbacks);
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
    AllocationAgent other = (AllocationAgent) obj;
    if (!java.util.Objects.equals(this.depot, other.depot))
      return false;
    if (!java.util.Objects.equals(this.taskAgentUUID, other.taskAgentUUID))
      return false;
    if (!java.util.Objects.equals(this.actual_customer_insert, other.actual_customer_insert))
      return false;
    if (other.number_agent_returned != this.number_agent_returned)
      return false;
    if (Double.doubleToLongBits(other.best_insertion_cost) != Double.doubleToLongBits(this.best_insertion_cost))
      return false;
    if (!java.util.Objects.equals(this.best_vehicle_insert, other.best_vehicle_insert))
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
    result = prime * result + java.util.Objects.hashCode(this.taskAgentUUID);
    result = prime * result + java.util.Objects.hashCode(this.actual_customer_insert);
    result = prime * result + Integer.hashCode(this.number_agent_returned);
    result = prime * result + Double.hashCode(this.best_insertion_cost);
    result = prime * result + java.util.Objects.hashCode(this.best_vehicle_insert);
    return result;
  }
  
  @SyntheticMember
  public AllocationAgent(final UUID parentID, final UUID agentID) {
    super(parentID, agentID);
  }
  
  @SyntheticMember
  @Inject
  public AllocationAgent(final UUID parentID, final UUID agentID, final DynamicSkillProvider skillProvider) {
    super(parentID, agentID, skillProvider);
  }
}
