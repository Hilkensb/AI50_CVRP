package fr.utbm.cvrp.solver;

import com.google.common.base.Objects;
import fr.utbm.cvrp.solver.AllocationAgent;
import fr.utbm.cvrp.solver.die;
import fr.utbm.cvrp.solver.finish;
import fr.utbm.cvrp.solver.nextCustomer;
import fr.utbm.cvrp.solver.nextCustomerRequest;
import fr.utbm.cvrp.solver.solution;
import io.sarl.core.AgentTask;
import io.sarl.core.Initialize;
import io.sarl.core.InnerContextAccess;
import io.sarl.core.Lifecycle;
import io.sarl.core.Logging;
import io.sarl.core.ParticipantJoined;
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
import io.sarl.lang.core.SpaceID;
import io.sarl.lang.util.SerializableProxy;
import java.io.ObjectStreamException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicInteger;
import javax.inject.Inject;
import org.eclipse.xtext.xbase.lib.Conversions;
import org.eclipse.xtext.xbase.lib.Extension;
import org.eclipse.xtext.xbase.lib.Procedures.Procedure1;
import org.eclipse.xtext.xbase.lib.Pure;

/**
 * Task Agent
 * <br>His goal is to give the customers to the allocation agent
 * <br>Strategies implemented: FIFO-ITER
 */
@SarlSpecification("0.12")
@SarlElementType(19)
@SuppressWarnings("all")
public class TaskAgent extends Agent {
  private UUID allocationAgentUUID;
  
  private String depot;
  
  private ConcurrentLinkedQueue<String> customers = new ConcurrentLinkedQueue<String>();
  
  private AtomicInteger vehicle_capacity = new AtomicInteger();
  
  private boolean allocation_agent_spawned = false;
  
  private ConcurrentLinkedQueue<ArrayList<String>> solution_found = new ConcurrentLinkedQueue<ArrayList<String>>();
  
  private void $behaviorUnit$Initialize$0(final Initialize occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.setLoggingName("Task Agent");
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("The agent has started.");
    Object _get = occurrence.parameters[0];
    this.depot = (_get == null ? null : _get.toString());
    Object _get_1 = occurrence.parameters[1];
    this.customers = ((ConcurrentLinkedQueue<String>) _get_1);
    Object _get_2 = occurrence.parameters[2];
    this.vehicle_capacity = ((AtomicInteger) _get_2);
    int lower_bound_vehicle = this.getLowerBoundVehiculeNumber(this.customers);
    this.allocationAgentUUID = UUID.randomUUID();
    Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.spawnInContextWithID(AllocationAgent.class, this.allocationAgentUUID, _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext(), this.depot, this.vehicle_capacity, Integer.valueOf(lower_bound_vehicle), this.getID());
  }
  
  private void $behaviorUnit$nextCustomerRequest$1(final nextCustomerRequest occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Next customer requested.");
    Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
    String _string = Integer.valueOf(((Object[])Conversions.unwrapArray(this.customers, Object.class)).length).toString();
    final AgentTask task = _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER.task(("waiting_for_allocation_agent" + _string));
    Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
    final Procedure1<Agent> _function = (Agent it) -> {
      if (this.allocation_agent_spawned) {
        boolean _isEmpty = this.customers.isEmpty();
        if ((!_isEmpty)) {
          Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
          _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_1.info("Sending the next customer.");
          String _nextCustomers = this.getNextCustomers();
          nextCustomer nextCustomerEvt = new nextCustomer(_nextCustomers);
          InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
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
          final Scope<Address> _function_1 = new Scope<Address>() {
            @Override
            public boolean matches(final Address it) {
              UUID _iD = it.getID();
              return Objects.equal(_iD, TaskAgent.this.allocationAgentUUID);
            }
            private Object writeReplace() throws ObjectStreamException {
              return new SerializableProxy($SerializableClosureProxy.class, TaskAgent.this.allocationAgentUUID);
            }
          };
          _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().emit(this.getID(), nextCustomerEvt, _function_1);
        } else {
          Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
          _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER_2.info("No more customer.");
          finish finishEvt = new finish();
          InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1 = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
          class $SerializableClosureProxy_1 implements Scope<Address> {
            
            private final UUID $_allocationAgentUUID_1;
            
            public $SerializableClosureProxy_1(final UUID $_allocationAgentUUID_1) {
              this.$_allocationAgentUUID_1 = $_allocationAgentUUID_1;
            }
            
            @Override
            public boolean matches(final Address it) {
              UUID _iD = it.getID();
              return Objects.equal(_iD, $_allocationAgentUUID_1);
            }
          }
          final Scope<Address> _function_2 = new Scope<Address>() {
            @Override
            public boolean matches(final Address it) {
              UUID _iD = it.getID();
              return Objects.equal(_iD, TaskAgent.this.allocationAgentUUID);
            }
            private Object writeReplace() throws ObjectStreamException {
              return new SerializableProxy($SerializableClosureProxy_1.class, TaskAgent.this.allocationAgentUUID);
            }
          };
          _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER_1.getInnerContext().getDefaultSpace().emit(this.getID(), finishEvt, _function_2);
        }
        Schedules _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_2 = this.$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER();
        _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_2.cancel(task);
      }
    };
    _$CAPACITY_USE$IO_SARL_CORE_SCHEDULES$CALLER_1.every(task, 100, _function);
  }
  
  private void $behaviorUnit$ParticipantJoined$2(final ParticipantJoined occurrence) {
    this.allocation_agent_spawned = true;
  }
  
  @SyntheticMember
  @Pure
  private boolean $behaviorUnitGuard$ParticipantJoined$2(final ParticipantJoined it, final ParticipantJoined occurrence) {
    InnerContextAccess _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER();
    SpaceID _spaceID = _$CAPACITY_USE$IO_SARL_CORE_INNERCONTEXTACCESS$CALLER.getInnerContext().getDefaultSpace().getSpaceID();
    boolean _equals = Objects.equal(occurrence.spaceID, _spaceID);
    return _equals;
  }
  
  private void $behaviorUnit$die$3(final die occurrence) {
    Logging _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LOGGING$CALLER.info("Killing myself.");
    Lifecycle _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER = this.$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER();
    _$CAPACITY_USE$IO_SARL_CORE_LIFECYCLE$CALLER.killMe();
  }
  
  private void $behaviorUnit$solution$4(final solution occurrence) {
    this.solution_found.add(occurrence.route);
  }
  
  /**
   * TaskAgent methods behavior
   */
  @Pure
  protected String getNextCustomers() {
    return this.customers.poll();
  }
  
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
  protected int getLowerBoundVehiculeNumber(final ConcurrentLinkedQueue<String> customersList) {
    int sum_demand = 0;
    for (final String customer : customersList) {
      int _demand = this.getDemand(customer);
      sum_demand = (sum_demand + _demand);
    }
    int _intValue = this.vehicle_capacity.intValue();
    int number_vehicle = Double.valueOf(Math.ceil((sum_demand / _intValue))).intValue();
    return number_vehicle;
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
  private void $guardEvaluator$nextCustomerRequest(final nextCustomerRequest occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$nextCustomerRequest$1(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$die(final die occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$die$3(occurrence));
  }
  
  @SyntheticMember
  @PerceptGuardEvaluator
  private void $guardEvaluator$ParticipantJoined(final ParticipantJoined occurrence, final Collection<Runnable> ___SARLlocal_runnableCollection) {
    assert occurrence != null;
    assert ___SARLlocal_runnableCollection != null;
    if ($behaviorUnitGuard$ParticipantJoined$2(occurrence, occurrence)) {
      ___SARLlocal_runnableCollection.add(() -> $behaviorUnit$ParticipantJoined$2(occurrence));
    }
  }
  
  @SyntheticMember
  @Override
  public void $getSupportedEvents(final Set<Class<? extends Event>> toBeFilled) {
    super.$getSupportedEvents(toBeFilled);
    toBeFilled.add(die.class);
    toBeFilled.add(nextCustomerRequest.class);
    toBeFilled.add(solution.class);
    toBeFilled.add(Initialize.class);
    toBeFilled.add(ParticipantJoined.class);
  }
  
  @SyntheticMember
  @Override
  public boolean $isSupportedEvent(final Class<? extends Event> event) {
    if (die.class.isAssignableFrom(event)) {
      return true;
    }
    if (nextCustomerRequest.class.isAssignableFrom(event)) {
      return true;
    }
    if (solution.class.isAssignableFrom(event)) {
      return true;
    }
    if (Initialize.class.isAssignableFrom(event)) {
      return true;
    }
    if (ParticipantJoined.class.isAssignableFrom(event)) {
      return true;
    }
    return false;
  }
  
  @SyntheticMember
  @Override
  public void $evaluateBehaviorGuards(final Object event, final Collection<Runnable> callbacks) {
    super.$evaluateBehaviorGuards(event, callbacks);
    if (event instanceof die) {
      final die occurrence = (die) event;
      $guardEvaluator$die(occurrence, callbacks);
    }
    if (event instanceof nextCustomerRequest) {
      final nextCustomerRequest occurrence = (nextCustomerRequest) event;
      $guardEvaluator$nextCustomerRequest(occurrence, callbacks);
    }
    if (event instanceof solution) {
      final solution occurrence = (solution) event;
      $guardEvaluator$solution(occurrence, callbacks);
    }
    if (event instanceof Initialize) {
      final Initialize occurrence = (Initialize) event;
      $guardEvaluator$Initialize(occurrence, callbacks);
    }
    if (event instanceof ParticipantJoined) {
      final ParticipantJoined occurrence = (ParticipantJoined) event;
      $guardEvaluator$ParticipantJoined(occurrence, callbacks);
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
    TaskAgent other = (TaskAgent) obj;
    if (!java.util.Objects.equals(this.allocationAgentUUID, other.allocationAgentUUID))
      return false;
    if (!java.util.Objects.equals(this.depot, other.depot))
      return false;
    if (other.allocation_agent_spawned != this.allocation_agent_spawned)
      return false;
    return super.equals(obj);
  }
  
  @Override
  @Pure
  @SyntheticMember
  public int hashCode() {
    int result = super.hashCode();
    final int prime = 31;
    result = prime * result + java.util.Objects.hashCode(this.allocationAgentUUID);
    result = prime * result + java.util.Objects.hashCode(this.depot);
    result = prime * result + Boolean.hashCode(this.allocation_agent_spawned);
    return result;
  }
  
  @SyntheticMember
  public TaskAgent(final UUID parentID, final UUID agentID) {
    super(parentID, agentID);
  }
  
  @SyntheticMember
  @Inject
  public TaskAgent(final UUID parentID, final UUID agentID, final DynamicSkillProvider skillProvider) {
    super(parentID, agentID, skillProvider);
  }
}
